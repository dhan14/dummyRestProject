from django.db import models
import pgtrigger


class DummyWarehouse(models.Model):
    warehouse_name = models.CharField(max_length=100, unique=True)
    warehouse_location = models.CharField(max_length=255)

    class Meta:
        db_table = "dra_warehouse"
        ordering = ['warehouse_name']
        indexes = [
            models.Index(fields=['warehouse_name'])
        ]


class DummyProduct(models.Model):
    product_name = models.CharField(max_length=255)
    desc = models.TextField()

    class Meta:
        db_table = "dra_product"
        ordering = ['product_name']
        indexes = [
            models.Index(fields=['product_name'])
        ]


class DummyInventory(models.Model):
    # id table ini otomatis
    id_warehouse = models.ForeignKey(
        DummyWarehouse,
        on_delete=models.CASCADE
    )
    id_product = models.ForeignKey(
        DummyProduct,
        on_delete=models.CASCADE
    )
    stock = models.IntegerField(default=0)

    class Meta:
        db_table = "dra_inventory"
        ordering = ['id_warehouse__id', 'id_product__id']
        indexes = [
            models.Index(fields=['id_warehouse', 'id_product']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['id_warehouse', 'id_product'],
                name='unique_inventory_item'
            ),
            models.CheckConstraint(
                check=models.Q(stock__gte=0),
                name='stock_must_be_non_negative'
            )
        ]


class DummyStockMovement(models.Model):
    # Field model
    TRANSACTION_TYPE_IN = 'IN'
    TRANSACTION_TYPE_OUT = 'OUT'

    warehouse = models.ForeignKey(
        'DummyWarehouse',
        on_delete=models.CASCADE,
        related_name='stock_movements'
    )
    product = models.ForeignKey(
        'DummyProduct',
        on_delete=models.CASCADE,
        related_name='stock_movements'
    )
    quantity = models.IntegerField()
    transaction_type = models.CharField(
        max_length=3,
        choices=[(TRANSACTION_TYPE_IN, 'IN'), (TRANSACTION_TYPE_OUT, 'OUT')]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "dra_stockmovement"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['warehouse', 'product']),
            models.Index(fields=['transaction_type']),
            models.Index(fields=['-created_at']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(quantity__gt=0),
                name='quantity_must_be_positive'
            )
        ]

    class triggers:
        # INSERT: Stock IN
        stock_in_insert = pgtrigger.Trigger(
            name='stock_in_insert',
            level=pgtrigger.Row,
            when=pgtrigger.After,
            operation=pgtrigger.Insert,
            condition=pgtrigger.Q(new__transaction_type='IN'),
            func='''
                INSERT INTO dra_inventory (id_warehouse_id, id_product_id, stock)
                VALUES (NEW.warehouse_id, NEW.product_id, NEW.quantity)
                ON CONFLICT (id_warehouse_id, id_product_id)
                DO UPDATE SET stock = dra_inventory.stock + EXCLUDED.stock;
                RETURN NEW;
            '''
        )
        # INSERT: Stock OUT
        stock_out_insert = pgtrigger.Trigger(
            name='stock_out_insert',
            level=pgtrigger.Row,
            when=pgtrigger.After,
            operation=pgtrigger.Insert,
            condition=pgtrigger.Q(new__transaction_type='OUT'),
            func='''
                UPDATE dra_inventory
                SET stock = stock - NEW.quantity
                WHERE id_warehouse_id = NEW.warehouse_i
                AND id_product_id = NEW.product_id;
                RETURN NEW;
            '''
        )
        # UPDATE: Rollback old, apply new
        stock_update = pgtrigger.Trigger(
            name='stock_update',
            level=pgtrigger.Row,
            when=pgtrigger.After,
            operation=pgtrigger.Update,
            func='''
                -- Rollback old transaction
                IF OLD.transaction_type = 'IN' THEN
                    UPDATE dra_inventory
                    SET stock = stock - OLD.quantity
                    WHERE id_warehouse_id = OLD.warehouse_i
                    AND id_product_id = OLD.product_id;
                ELSE
                    UPDATE dra_inventory
                    SET stock = stock + OLD.quantity
                    WHERE id_warehouse_id = OLD.warehouse_i
                    AND id_product_id = OLD.product_id;
                END IF;
                -- Apply new transaction
                IF NEW.transaction_type = 'IN' THEN
                    INSERT INTO dra_inventory (id_warehouse_id, id_product_id, stock)
                    VALUES (NEW.warehouse_id, NEW.product_id, NEW.quantity)
                    ON CONFLICT (id_warehouse_id, id_product_id)
                    DO UPDATE SET stock = dra_inventory.stock + EXCLUDED.stock;
                ELSE
                    UPDATE dra_inventory
                    SET stock = stock - NEW.quantity
                    WHERE id_warehouse_id = NEW.warehouse_i
                    AND id_product_id = NEW.product_id;
                END IF;
                RETURN NEW;
            '''
        )
        # DELETE: Rollback transaction
        stock_delete = pgtrigger.Trigger(
            name='stock_delete',
            level=pgtrigger.Row,
            when=pgtrigger.After,
            operation=pgtrigger.Delete,
            func='''
                IF OLD.transaction_type = 'IN' THEN
                    UPDATE dra_inventory
                    SET stock = stock - OLD.quantity
                    WHERE id_warehouse_id = OLD.warehouse_i
                    AND id_product_id = OLD.product_id;
                ELSE
                    UPDATE dra_inventory
                    SET stock = stock + OLD.quantity
                    WHERE id_warehouse_id = OLD.warehouse_i
                    AND id_product_id = OLD.product_id;
                END IF;
                RETURN OLD;
            '''
        )
