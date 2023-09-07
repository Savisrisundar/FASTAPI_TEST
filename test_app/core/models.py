from pydantic import BaseModel
class HealthCheck(BaseModel):
    #healthcheck model
    name:str
    status:bool=True
    
    def __str__(self):
        return self.name