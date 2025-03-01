#Marzieh Saberi
#Date: Dec 2023
#Mastermind Test
#-------------------------------------------------------------

from Mastermind import Code_Breaker

#Test Score-------------------------------------------------------------
def TestScore():
    print("Test Score:")
    try:
        code_breaker1 = Code_Breaker(0, True, "test", 0, 91, 2, "win", [], [], [[1, 1, 1, 0, 0], [2, 2, 2, 2, 0], [2, 2, 1, 1, 0], [2, 2, 2, 1, 0], [2, 2, 2, 2, 2]], 4, [])
        assert code_breaker1.CalculateScore() == 689
        print("Test Score 1: OK")
    except AssertionError:
        print("Error 1: The score function does not work properly!")

    try:
        code_breaker2 = Code_Breaker(0, True, "test", 0, 42, 0, "lose", [], [], [[2, 0, 0, 0, 0], [1, 1, 1, 0, 0], [1, 1, 1, 0, 0], [1, 1, 1, 0, 0], [2, 2, 1, 0, 0], [2, 2, 2, 2, 0]], 6, [])
        assert code_breaker2.CalculateScore() == 120
        print("Test Score 2: OK")
    except AssertionError:
        print("Error 2: The score function does not work properly!")

    try:
        code_breaker3 = Code_Breaker(0, True, "test", 0, 126, 1, "lose", [], [], [[1, 1, 0, 0, 0], [2, 1, 0, 0, 0], [2, 2, 2, 0, 0], [2, 2, 1, 0, 0], [2, 2, 1, 0, 0], [1, 0, 0, 0, 0], [2, 2, 1, 0, 0], [2, 2, 2, 0, 0], [2, 2, 2, 1, 1], [2, 2, 2, 2, 0], [2, 2, 2, 0, 0], [2, 2, 2, 1, 0]], 11, [])
        assert code_breaker3.CalculateScore() == 160
        print("Test Score 3: OK")
    except AssertionError:
        print("Error 3: The score function does not work properly!")

    try:
        code_breaker3 = Code_Breaker(0, True, "test", 0, 84, 1, "win", [], [], [[2, 0, 0, 0, 0], [0, 0, 0, 0, 0], [2, 2, 0, 0, 0], [0, 0, 0, 0, 0], [2, 0, 0, 0, 0], [2, 2, 0, 0, 0], [2, 2, 0, 0, 0], [2, 0, 0, 0, 0], [2, 1, 0, 0, 0], [2, 1, 1, 0, 0], [2, 1, 1, 0, 0], [2, 2, 2, 2, 2]], 11, [])
        assert code_breaker3.CalculateScore() == 589
        print("Test Score 4: OK")
    except AssertionError:
        print("Error 4: The score function does not work properly!")
        
    print("-----------------------------------")
    return

#Test KeyBreakerPeg-------------------------------------------------------------      
def TestKeyBreakerPeg():
    print("\nTest KeyBreakerPeg:")

    try:
        code_breaker2 = Code_Breaker(0, True, "test", 0, 0, 0, "lose", [8, 4, 3, 7, 5], [[4, 7, 6, 9, 0]], [], 0, [])
        assert code_breaker2.AppendKeyBreakerPeg() == [1, 1, 0, 0, 0]
        print("Test KeyBreakerPeg 1: OK")
    except AssertionError:
        print("Error 1: The KeyBreakerPeg function does not work properly!")
        
    try:
        code_breaker2 = Code_Breaker(0, True, "test", 0, 0, 0, "lose", [9, 2, 3, 6, 1], [[2, 3, 5, 6, 8]], [], 0, [])
        assert code_breaker2.AppendKeyBreakerPeg() == [2, 1, 1, 0, 0]
        print("Test KeyBreakerPeg 2: OK")
    except AssertionError:
        print("Error 2: The KeyBreakerPeg function does not work properly!")
    
    try:
        code_breaker2 = Code_Breaker(0, True, "test", 0, 0, 0, "lose", [2, 7, 1, 0, 8], [[7, 7, 2, 1, 1]], [], 0, [])
        assert code_breaker2.AppendKeyBreakerPeg() == [2, 1, 1, 0, 0]
        print("Test KeyBreakerPeg 3: OK")
    except AssertionError:
        print("Error 3: The KeyBreakerPeg function does not work properly!")
    
    try:
        code_breaker1 = Code_Breaker(0, True, "test", 0, 0, 0, "lose", [5, 4, 1, 9, 9], [[9, 5, 1, 1, 9]], [], 0, [])
        assert code_breaker1.AppendKeyBreakerPeg() == [2, 2, 1, 1, 0]
        print("Test KeyBreakerPeg 4: OK")
    except AssertionError:
        print("Error 4: The KeyBreakerPeg function does not work properly!")
    
    try:
        code_breaker2 = Code_Breaker(0, True, "test", 0, 0, 0, "lose", [5, 8, 7, 9, 7], [[7, 7, 8, 2, 7]], [], 0, [])
        assert code_breaker2.AppendKeyBreakerPeg() == [2, 1, 1, 0, 0]
        print("Test KeyBreakerPeg 5: OK")
    except AssertionError:
        print("Error 5: The KeyBreakerPeg function does not work properly!")
    
    try:
        code_breaker3 = Code_Breaker(0, True, "test", 0, 0, 0, "lose", [5, 0, 0, 3, 4], [[0, 0, 0, 4, 4]], [], 0, [])
        assert code_breaker3.AppendKeyBreakerPeg() == [2, 2, 2, 0, 0]
        print("Test KeyBreakerPeg 6: OK")
    except AssertionError:
        print("Error 6: The KeyBreakerPeg function does not work properly!")
        
    print("-----------------------------------")
    return

#Main-------------------------------------------------------------     
def main():    
    TestScore()
    TestKeyBreakerPeg()

if __name__ == '__main__':
    main()
