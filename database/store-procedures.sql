CREATE PROCEDURE minus_order 
    @product_id BIGINT, 
    @supplier_id BIGINT, 
    @quantity_ordered INTEGER
AS
BEGIN
    UPDATE product_availability
    SET quantity_available = quantity_available - @quantity_ordered
    WHERE product_id = @product_id AND supplier_id = @supplier_id;

    IF @@ROWCOUNT = 0
    BEGIN
        RAISERROR('Product or supplier not found, or insufficient quantity available', 16, 1);
    END
END;
GO;
