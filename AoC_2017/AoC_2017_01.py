import blitzen


@blitzen.run
def main(input_string, verbose=False):
    captcha = [int(i) for i in input_string]
    cl = len(captcha)
    captcha += captcha[:cl // 2]
    p1 = sum([a for a, b in zip(captcha[:cl], captcha[1:]) if a == b])
    p2 = sum([a for a, b in zip(captcha, captcha[cl // 2:]) if a == b])
    return p1, p2

