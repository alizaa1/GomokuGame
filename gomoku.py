
def is_empty(board):
    for i in range (len(board)):
        for j in range (len(board[0])):

            if board[i][j] != " ":
                return False

    return True

def is_bounded(board, y_end, x_end, length, d_y, d_x):

# Determine start position
    y_start = y_end - ((length - 1) * d_y)
    x_start = x_end - ((length - 1) * d_x)

# Determine positions before and after the sequence
    y_prev = y_start - d_y
    x_prev = x_start - d_x

    y_after = y_end + d_y
    x_after = x_end + d_x

# Check if after and previous values are within bounds and is empty
    prev_is_open = False
    after_is_open = False

    if 0 <= y_prev < len(board) and 0 <= x_prev < len(board[0]):
        if board[y_prev][x_prev] == " ":
            prev_is_open = True

        else:
            prev_is_open = False

    if 0 <= y_after < len(board) and 0 <= x_after < len(board[0]):
        if board[y_after][x_after] == " ":
            after_is_open = True

        else:
            after_is_open = False

# Check open, semiopen, or closed
    if prev_is_open and after_is_open:
        return "OPEN"

    elif prev_is_open or after_is_open:
        return "SEMIOPEN"

    else:
        return "CLOSED"

def detect_row(board, col, y_start, x_start, length, d_y, d_x):

# Initialize counters
    cur_length = 0
    open_seq_count = 0
    semi_open_seq_count = 0

# Check if within board boundaries
    while 0 <= y_start < len(board) and 0 <= x_start < len(board[0]):
        if board[y_start][x_start] == col:
            cur_length += 1

        # Checks if sequence is open or semiopen, then increment the respective count, and reset cur_length to search for new sequence
            if cur_length == length:
                start_y = y_start + d_y
                start_x = x_start + d_x
                end_y = y_start - ((length - 1) * d_y) - d_y
                end_x = x_start - ((length - 1) * d_x) - d_x

                start_is_open = 0 <= start_y < len(board) and 0 <= start_x < len(board[0]) and board[start_y][start_x] == " "
                end_is_open = 0 <= end_y < len(board) and 0 <= end_x < len(board[0]) and board[end_y][end_x] == " "

                # Check if open
                if start_is_open and end_is_open:
                    open_seq_count += 1

                    # problem: we are counting subseq of seq of same colour
                    # basically u need to check even if its semi open whatevers blocking it
                    # you have to check if its a diff color bc if its the same its a subsequence
                # Check if semi-open
                elif start_is_open or end_is_open:
                    if board[start_y][start_x] == col or board[end_y][end_x] == col:
                        semi_open_seq_count += 0

                    else:
                        semi_open_seq_count += 1

                cur_length = 0

        else:
            cur_length = 0

        # Increment position
        y_start += d_y
        x_start += d_x

    return open_seq_count, semi_open_seq_count

def detect_rows(board, col, length):
    open_seq_count, semi_open_seq_count = 0, 0
    all_directions = [[0, 1], [1, 0], [1, 1], [1, -1]]

    for y in range(len(board)):
        for x in range(len(board[0])):
            for d_y, d_x in all_directions:
                cur_length = 0
                temp_y = y
                temp_x = x

                while 0 <= temp_y < len(board) and 0 <= temp_x < len(board[0]):
                    if board[temp_y][temp_x] == col:

                        cur_length += 1

                        if cur_length == length:
                            start_y = temp_y + d_y
                            start_x = temp_x + d_x
                            end_y = temp_y - ((length - 1) * d_y) - d_y
                            end_x = temp_x - ((length - 1) * d_x) - d_x

                            start_is_open = 0 <= start_y < len(board) and 0 <= start_x < len(board[0]) and board[start_y][start_x] == " "
                            end_is_open = 0 <= end_y < len(board) and 0 <= end_x < len(board[0]) and board[end_y][end_x] == " "

                            if start_is_open and end_is_open:
                                open_seq_count += 1

                            elif start_is_open or end_is_open:

                                if (0 <= start_y < len(board) and 0 <= start_x < len(board[0])) and (0 <= end_y < len(board) and 0 <= end_x < len(board[0])):

                                    if board[start_y][start_x] == col or board[end_y][end_x] == col:
                                        semi_open_seq_count += 0

                                    else:
                                        semi_open_seq_count += 1

                                else:
                                    semi_open_seq_count += 1
                                    break
                    else:
                        break


                    temp_y += d_y
                    temp_x += d_x

    return open_seq_count, semi_open_seq_count

def search_max(board):

    max_score = -10000000000

    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == " ":
                board[y][x] = "b"  # Try placing a black stone
                the_score = score(board) # the_score = theoretical score :)

                if the_score > max_score:
                    max_score = the_score
                    move_y = y
                    move_x = x

                board[y][x] = " "  # Undo the move

    return move_y, move_x

def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)

    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])

def check_win(board, y, x, col, length):
    all_directions = [[0, 1], [1, 0], [1, 1], [1, -1]]

    for d_y, d_x in all_directions:
        seq_length = 0
        for i in range(length):
            new_y = y + (i * d_y)
            new_x = x + (i * d_x)
            if 0 <= new_y < len(board) and 0 <= new_x < len(board[0]) and board[new_y][new_x] == col:
                seq_length += 1
            else:
                break
        if seq_length == length:
            return True
    return False

def is_win(board):
    col = ["b", "w"]

# Iterates through each position on the board
    for colour in col:
        for y in range(len(board)):
            for x in range(len(board[0])):

# If a black or white closed sequence exists, player wins
                if check_win(board, y, x, colour, 5) and colour == "b":
                    return "Black won"
                elif check_win(board, y, x, colour, 5) and colour == "w":
                    return "White won"

    for i in range (len(board)):
        for j in range (len(board[0])):
            if board[i][j] == " ":
                return "CONTINUE PLAYING"

    return "DRAW"

def print_board(board):
    s = "*"
# Column Headers
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"

    s += str((len(board[0])-1)%10)
    s += "*\n"

# Row Headers
    for i in range(len(board)):
        s += str(i%10)

        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"

        s += str(board[i][len(board[0])-1])
        s += "*\n"

# Bottom Border
    s += (len(board[0])*2 + 1)*"*"

    print(s)

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board

def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))

def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res

        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res

def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x

def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0  WRONG
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1 WRONG
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0 WRONG
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1 WRONG
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0 WRONG
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0 WRONG
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1 WRONG
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0

if __name__ == "__main__":
    easy_testset_for_main_functions()