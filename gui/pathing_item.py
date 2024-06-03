from gui.menu_item import MenuItem


class PathingItem(MenuItem):
    def update_selection(self, clicked_pos: (int, int)) -> None:
        super().update_selection(clicked_pos)
        if self.is_selected:
            self.owner.set_pathing_item(self)
