# proof
modular jwt auth for flask so you don't have to worry about login

## what is it
a plug-and-play authentication system for flask apps that uses jwts. fast game. modular so you can drop it into your
project as-is

## features
- modular - drop it in and it just works
- jwt based - no messy sessions or database bloat for every request
- secure - handles the heavy lifting so you don't accidentally leave the door open
- flask native - belongs in your app

## how to get it going
```bash
pip install -r requirements.txt
python run.py
```

## how to use it
just import the auth module and wrap your routes. simple
```python
@app.route('/super-duper-secret-stuff')
@jwt_required
def secret():
    return {'message': 'you\'re in'}
```

## contribute
let me know if your thoughts!