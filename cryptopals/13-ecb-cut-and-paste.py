import random

print("""
____________________________
ECB cut-and-paste

Write a k=v parsing routine, as if for a structured cookie. The routine should take:

foo=bar&baz=qux&zap=zazzle

... and produce:

{
  foo: 'bar',
  baz: 'qux',
  zap: 'zazzle'
}

(you know, the object; I don't care if you convert it to JSON).

Now write a function that encodes a user profile in that format, given an email address. You should have something like:

profile_for("foo@bar.com")

... and it should produce:

{
  email: 'foo@bar.com',
  uid: 10,
  role: 'user'
}

... encoded as:

email=foo@bar.com&uid=10&role=user

Your "profile_for" function should not allow encoding metacharacters (& and =). Eat them, quote them, whatever you want to do, but don't let people set their email address to "foo@bar.com&role=admin".

Now, two more easy functions. Generate a random AES key, then:

    Encrypt the encoded user profile under the key; "provide" that to the "attacker".
    Decrypt the encoded user profile and parse it.

Using only the user input to profile_for() (as an oracle to generate "valid" ciphertexts) and the ciphertexts themselves, make a role=admin profile. 
____________________________
""")


def params_to_dict(params):

    final_dict = {}
    arr = params.split("&")

    for elmt in arr:
        key,value = elmt.split("=")
        final_dict[key] = value

    return final_dict

def profile_for(email):
    uid = random.randint(1,100)
    role = "user"
    email = email.replace("&","").replace("=","")
    return f"email={email}&uid={uid}&role={role}"

print()

res = params_to_dict("foo=bar&baz=qux&zap=zazzle")
print(res)

res = profile_for("foo@bar.com")
print(res)