script = """
drop view if exists parent_children;
CREATE VIEW parent_children (parent, children, root, cond) AS
(   SELECT jsonb_build_object('id', p.id,'name', p.name, 'type', p.type, 'date', p.date, 'price', p.price, 'parentId',p.parentid, 'children', '[]' :: jsonb) :: text AS parent
         , jsonb_agg(jsonb_build_object('id', c.id,'name', c.name, 'type', c.type, 'date', c.date, 'price', c.price, 'parentId',c.parentid, 'children', '[]' :: jsonb)) :: text AS children
         , array[c.parentid] AS root
         , array[c.parentid] AS cond
      FROM public.shopunits AS c
      LEFT JOIN public.shopunits AS p
        ON p.id = c.parentid
     GROUP BY  p.name, p.id, c.parentid
) ;

WITH RECURSIVE list(parent, children, root, cond) AS
(   SELECT parent, children, root, cond
      FROM parent_children
     WHERE root = array['%s']::uuid[]  -- start with the root parents
    UNION
    SELECT p.parent
         , replace(p.children, c.parent, replace(c.parent, '[]', c.children))
         , p.root
         , p.cond || c.cond
      FROM list AS p
     INNER JOIN parent_children AS c
        ON position(c.parent IN p.children) > 0
       AND NOT p.cond @> c.root -- condition to avoid circular path
)
SELECT children :: jsonb
  FROM list AS l
  ORDER BY array_length(cond, 1) DESC
  LIMIT 1 ;
"""