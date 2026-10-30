## Tests

Put tests in `Tests/test_*.py` files. Test functions must start with `test_` and accept a `board` argument. The runner gives each test a fresh board.

Run all tests from the project root:

```sh
python3 -m Tests.runner
```

For the graphical version of the game, be sure to install pygame==2.6.1 with 
```sh
python3 -m pip install pygame==2.6.1
```