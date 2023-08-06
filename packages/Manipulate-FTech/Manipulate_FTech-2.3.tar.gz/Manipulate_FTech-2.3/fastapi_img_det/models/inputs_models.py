from pydantic import BaseModel


class ImageHash(BaseModel):
#    params: ImageHash = None
        img: str
