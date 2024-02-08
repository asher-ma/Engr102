errors = []

<<<<<<< HEAD
#try:
#    import mysql
#except ModuleNotFoundError as e:
#    errors.append(str(e))

=======
>>>>>>> 99cdceb0938790b910c6134eb2f4760cd168f06b
try:
    import bs4
except ModuleNotFoundError as e:
    errors.append(str(e))

try:
    import requests
except ModuleNotFoundError as e:
    errors.append(str(e))

try:
    import pandas
except ModuleNotFoundError as e:
    errors.append(str(e))

if not errors:
    print("No Issues Detected")
else:
    print("\n".join(errors))