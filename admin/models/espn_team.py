from dataclasses import dataclass

@dataclass
class EspnTeam:
    flag: str
    name: str
    image_url: str
    id: str
    slug: str

    def to_fire_doc(self):
        return {
            'flag': self.flag,
            'name': self.name,
            'image_url': self.image_url,
            'id': self.id,   
        }