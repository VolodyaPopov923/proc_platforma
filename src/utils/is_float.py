def is_float(num: str):
    num = num.replace(',', '.')
    
    try:
        float(num)
        return True
    except:
        False