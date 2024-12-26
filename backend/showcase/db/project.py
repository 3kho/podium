from pydantic import BaseModel, HttpUrl, Field, StringConstraints
from pydantic.json_schema import SkipJsonSchema
from typing import Annotated, List, Optional

# https://docs.pydantic.dev/1.10/usage/schema/#field-customization
class ProjectCreationPayload(BaseModel):
    name: str
    readme: HttpUrl
    repo: HttpUrl
    image_url: HttpUrl
    description: Optional[str] = None
    
    owner: Annotated[SkipJsonSchema[List[str]], Field()] = None
    # https://docs.pydantic.dev/latest/api/types/#pydantic.types.constr--__tabbed_1_2
    event: List[str] | Annotated[str, StringConstraints(
            pattern=r'^rec\w*$'
        )]
    # join_code: SkipJsonSchema[str] = None

    def model_dump(self, *args, **kwargs):
        data = super().model_dump(*args, **kwargs)
        data['readme'] = str(self.readme)
        data['repo'] = str(self.repo)
        data['image_url'] = str(self.image_url)
        return data
    
class Project(ProjectCreationPayload):
    id: str
    points: int