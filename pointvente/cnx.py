# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 21:38:01 2019

@author: hp pc
"""
 
import pyodbc

class connexion:
    
    
    def __init__(self):#methode constructeur
        
        self.cnx=pyodbc.connect("DRIVER=SQL Server;SERVER=10.45.0.11\FRONTRES;PORT=1433;UID=sa;PWD=Leon2017;DATABASE=STOCKCFDB")
        # self.cnx=pyodbc.connect("DRIVER=SQL Server;SERVER=127.0.0.1;PORT=1433;UID=sa;PWD=dev;DATABASE=DbBB")
            #initailisation du connexion
        self.cur=self.cnx.cursor()#obtention du curseur
    
    
    def Mise(self,rqt):#methode mise à jour avec la param rqt
        
            
        try:
#            if self.cnx is None:
#                print("salut")
            self.cur.execute(rqt[0],rqt[1])#execution du requete
            self.cnx.commit()#validation du requete
            return True #return True
        except pyodbc.DatabaseError as e:
            print("Error ", e)
            return False
#        finally:
#            self.cur.close()
#            self.cnx.close()
        
        
    def Selection(self,rqt):
        try:
            
#            if self.cnx is None:
#                print("salut")
 
            if len(rqt)>1:
                self.cur.execute(rqt[0],rqt[1])
            else:
                self.cur.execute(rqt[0])
            # self.cnx.commit()
            return self.cur
        except pyodbc.DatabaseError as e:
            print("Error ", e)
            return 0
#        finally:
#            self.cur.close()
#            self.cnx.close()