from game import Game

g = Game()

g.show_start_screen()
while g.running:
    g.curr_menu.display_menu()
    g.new()
    g.run()
    
g.show_go_screen()
