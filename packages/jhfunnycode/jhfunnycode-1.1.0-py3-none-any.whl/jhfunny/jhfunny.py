class funny:
    def starpix(self, star_index, updown="up"):
        self.index = star_index
        self.updown = updown
        
        if updown == "up":
            i = 0
            while i <= star_index:
                print("*"*i)
                i += 1
                
        elif updown == "down":
            i = 0
            miner_idx = star_index
            while i <= star_index:
                print("*"*miner_idx)
                miner_idx -= 1
                i += 1

