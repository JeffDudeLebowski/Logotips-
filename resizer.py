for p, s, fs in os.walk ("International/England 1"):
    
    
    for f in fs:
        if f[-4:].lower() == ".png":
            fname = os.path.join(p, f)
            print (fname)
            try:
                img = Image.open(fname)

                w0 = img.size[0]
                h0 = img.size[1] 

                if h0 > w0:
                    h1 = h0
                    w1 = h1
                else:

                    w1 = w0
                    h1 = w1
                x1 = -(w1 - w0)//2
                y1 = -(h1 - h0)//2

                img_new = img.transform((w1, h1), Image.EXTENT, (x1,y1,x1+w1,y1+h1)) 



                fnameparts = os.path.splitext(fname)
                fnamesq=fnameparts[0] +'_sq_' + fnameparts[1]
                img_new.save(fnamesq)
            except Exception:
                print("error while processing")
