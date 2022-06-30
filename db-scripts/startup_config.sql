CREATE or replace FUNCTION updateprice() RETURNS trigger AS $update_price$

    declare
    count integer := (select sum(price) from shopunits where parentid=NEW.parentid);
    summ integer := (select count(*) from shopunits where parentid=NEW.parentid);
    BEGIN
        IF NEW.price IS NULL THEN
            NEW.price:=0;
        END IF;

        UPDATE shopunits set price=count / summ where id = NEW.parentid; 
        RETURN NEW;
    END
$update_price$ LANGUAGE plpgsql;


CREATE TRIGGER update_price AFTER INSERT OR UPDATE ON shopunits
    FOR EACH ROW EXECUTE PROCEDURE update_price();
-- 
CREATE VIEW parent_children (parent, children, root, cond) AS (
SELECT jsonb_build_object('id', p.id, 'name', p.name, 'type', p.type, 'date', p.date, 'price', p.price, 'parentId', p.parentid, 'children', '[]'::jsonb)::text AS parent,
    jsonb_agg(jsonb_build_object('id', c.id, 'name', c.name, 'type', c.type, 'date', c.date, 'price', c.price, 'parentId', c.parentid, 'children', '[]'::jsonb))::text AS children,
    ARRAY[c.parentid] AS root,
    ARRAY[c.parentid] AS cond
   FROM shopunits c
     LEFT JOIN shopunits p ON p.id = c.parentid
  GROUP BY p.name, p.id, c.parentid
  );