class ProgressBar:
    
    print_percent = False
    max_char_length = 80
    bar_char = "#"
    ENABLE_PERCENT = True
    DISABLE_PERCENT = False
    
    def __init__(self, print_percent=False, max_char_length=80, bar_char = "#"):
        self.print_percent = print_percent
        self.max_char_length = max_char_length
        self.bar_char = bar_char
        
    
    def printBar(self, min_val, max_val):
        percentage = (min_val * 100) / max_val
        
        if self.print_percent:
            bar_length = self.max_char_length - 11
            endchar = ""
        else:
            bar_length = self.max_char_length - 3
            endchar = "\r"
            
        progress = int(bar_length * (percentage / 100))
        percentage_value = str(round(percentage, 1))
        
        progress_bar = (self.bar_char * progress) + (" " * (bar_length - progress))
        print(f" [{progress_bar}]", end=endchar)
        
        if self.print_percent:
            percent_string = f" {percentage_value}%".rjust(8)
            print(f"{percent_string}", end="\r")
        