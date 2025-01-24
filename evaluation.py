class Evaluation:
    def __init__(self):
        pass

    def evaluate(self, board):
        
        aggregate_height = self.calculate_aggregate_height(board)
        complete_lines = self.count_complete_lines(board)
        holes = self.count_holes(board)
        bumpiness = self.calculate_bumpiness(board)

        # Weighted evaluation
        return (
            -0.510066 * aggregate_height +
            0.760666 * complete_lines +
            -0.35663 * holes +
            -0.184483 * bumpiness
        )

    def calculate_aggregate_height(self, board):
        """Calculate the sum of the heights of all columns."""
        heights = [self.get_column_height(board, col) for col in range(board.width)]
        return sum(heights)

    def count_complete_lines(self, board):
        complete_lines = 0
        for row in board.board:
            if all(cell["fill"] for cell in row):
                complete_lines += 1
        return complete_lines

    def count_holes(self, board):
        holes = 0
        for col in range(board.width):
            filled = False
            for row in board.board:
                if row[col]["fill"]:
                    filled = True
                elif filled and not row[col]["fill"]:
                    holes += 1
        return holes

    def calculate_bumpiness(self, board):
        """Calculate the difference in heights between adjacent columns."""
        heights = [self.get_column_height(board, col) for col in range(board.width)]
        bumpiness = sum(abs(heights[i] - heights[i + 1]) for i in range(len(heights) - 1))
        return bumpiness

    def get_column_height(self, board, col):
        """Get the height of a specific column."""
        for row_idx, row in enumerate(reversed(board.board)):
            if row[col]["fill"]:
                return board.height - row_idx
        return 0
