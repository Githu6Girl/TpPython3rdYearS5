from dataclasses import dataclass
from typing import List, Set

@dataclass(frozen=True)
class Post:
    author: str
    content: str

class User:
    def __init__(self, name: str):
        self.name = name
        self._followers: Set["User"] = set()     # ONLY this is stored
        self._notifications: List[Post] = []

    def update(self, post: Post) -> None:
        self._notifications.append(post)

    def follow(self, other: "User") -> None:
        if other is not self:
            other._followers.add(self)           # add self as follower of other

    def unfollow(self, other: "User") -> None:
        other._followers.discard(self)

    def post(self, content: str) -> Post:
        new_post = Post(author=self.name, content=content)
        for follower in list(self._followers):
            follower.update(new_post)
        return new_post

    def notifications(self) -> List[Post]:
        return list(self._notifications)

    def followers(self) -> Set["User"]:
        return set(self._followers)

    # NO following() method here

if __name__ == "__main__":
    meriem = User("meriem")
    malak = User("malak")
    dalila = User("dalila")

    dalila.follow(meriem)
    malak.follow(meriem)

    meriem.post("Hello, world!")

    dalila.follow(malak)
    malak.post("New day, new me!")

    # Option B: derive following transiently
    def derived_following(me: User, everyone: Set[User]) -> Set[User]:
        return {u for u in everyone if me in u.followers() and u is not me}

    everyone = {meriem, malak, dalila}
    print("dalila follows:", {u.name for u in derived_following(dalila, everyone)})

    for p in dalila.notifications():
        print(f"[dalila feed] {p.author}: {p.content}")

