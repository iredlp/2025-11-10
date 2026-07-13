from database.DB_connect import DBConnect
from model.arco import Arco
from model.ordine import Ordine
from model.store import Store

class DAO():
    @staticmethod
    def getAllStores():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * from stores"

        cursor.execute(query)

        for row in cursor:
            results.append(Store(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(store):
        # from model.anno import Anno
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select o.*
                    from orders o , stores s 
                    where s.store_name =%s and o.store_id  =s.store_id """

        cursor.execute(query, (store, ))

        for row in cursor:
            results.append(Ordine(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(store,k, idMapC):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT 
            o1.order_id AS o1, 
            o2.order_id AS o2,
            CAST(t1.tot_items + t2.tot_items AS FLOAT) / DATEDIFF(o2.order_date, o1.order_date) AS peso
        FROM 
            orders o1, orders o2, stores s,
            (SELECT order_id, SUM(quantity) AS tot_items FROM order_items GROUP BY order_id) t1,
            (SELECT order_id, SUM(quantity) AS tot_items FROM order_items GROUP BY order_id) t2
        WHERE 
            s.store_name = %s 
            AND o1.store_id = s.store_id 
            AND o2.store_id = s.store_id 
            AND o1.order_id = t1.order_id
            AND o2.order_id = t2.order_id
            AND o1.order_date < o2.order_date 
            AND DATEDIFF(o2.order_date, o1.order_date) <= %s
        ORDER BY 
            o1.order_id, o2.order_id"""

        cursor.execute(query, (store, k))

        for row in cursor:
            ordine1 = idMapC.get(row['o1'])
            ordine2 = idMapC.get(row['o2'])
            # Aggiungi l'arco SOLO SE entrambi i costruttori sono nodi validi del grafo
            if  ordine1 is not None and ordine2 is not None:
                # costruttore1 =  idMapC[row['a1']]
                # costruttore2 =idMapC [row['a2']]

                # Crei l'arco passando gli oggetti, non gli ID numerici
                results.append(Arco(o1= ordine1, o2=ordine2, peso=row['peso']))
        # results.append(Arco(**row))

        cursor.close()
        conn.close()
        return results