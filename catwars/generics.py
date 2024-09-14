import pygame

class GroupWithDispatch(pygame.sprite.Group):
    """Generic sprite group that supports dispatch method."""
    def dispatch(self, event):
        """Process given event by all members of the group."""
        for member in self:
            member.dispatch(event)

