from gui.menu_item import MenuItem


class StartItem(MenuItem):
    def update_selection(self, clicked_pos: (int, int)) -> None:
        super().update_selection(clicked_pos)
        if self.is_selected and self.owner.is_ready():
            self.owner.set_start()
