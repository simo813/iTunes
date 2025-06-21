from database.DB_connect import DBConnect
from model.album import Album


class DAO():

    @staticmethod
    def getNodes(duration):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select a.AlbumId , a.Title , sum(t.Milliseconds)/(1000*60) as duration
                        from itunes.album a , itunes.track t 
                        where a.AlbumId = t.AlbumId 
                        group by a.AlbumId , a.Title
                        having sum(t.Milliseconds)/(1000*60) > %s
                        """
            cursor.execute(query, (duration, ))

            for row in cursor:
                result.append(Album(row["AlbumId"], row["Title"], row["duration"]))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getEdge(AlbumId1, AlbumId2):
        cnx = DBConnect.get_connection()
        result = None
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select count(*) as cont
                        from itunes.playlisttrack p , itunes.track t  , itunes.playlisttrack p2, itunes.track t2
                        where 	t.AlbumId = %s
                                and t2.AlbumId = %s
                                and t.trackId = p.trackId
                                and t2.trackId = p2.trackId
                                and p.PlaylistId = p2.PlaylistId
                                and p.TrackId <> p2.TrackId
                                                    """
            cursor.execute(query, (AlbumId1, AlbumId2))

            row = cursor.fetchone()
            result= int(row["cont"])
            cursor.close()
            cnx.close()
        return result
