import pygame

class GroupWithDispatch(pygame.sprite.Group):
    """Generic sprite group that supports dispatch method."""
    def dispatch(self, event):
        """Process given event by all members of the group. Returns True when some member decides nobody else needs to process the event now."""
        for member in self:
            if member.dispatch(event):
                return True

