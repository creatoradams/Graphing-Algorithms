import sys
import Task1
import Task2
import Task3

def call_run(mod):

    # module level run()
    if hasattr(mod, "run") and callable(mod.run):
        return mod.run()

   # fallback: try a class with a run()
    for name in ("Task1", "Task2", "Task3", "Main", "Runner"):
        cls = getattr(mod, name, None)
        if cls is None:
            continue
        # try static/class method
        try:
            return cls.run()
        except Exception:
            pass
        # try instance method
        try:
            return cls().run()
        except Exception:
            pass

def run_choice(choice: str):
    choice = (choice or "").strip().lower()
    if choice in ("1", "task1"):
        call_run(Task1)
    elif choice in ("2", "task2"):
        call_run(Task2)
    elif choice in ("3", "task3"):
        call_run(Task3)
    elif choice in ("all", "a"):
        call_run(Task1)
        call_run(Task2)
        call_run(Task3)
    elif choice in ("0"):
        return False
    else:
        print("Please enter 1, 2, 3, all, or 0.")
    return True

def main():
    # Allow CLI arg: python Main.py 2
    if len(sys.argv) > 1:
        run_choice(sys.argv[1])
        return

    # Interactive prompt
    while True:
        ans = input("Run which task? [1, 2, 3, all, or 0 to exit]: ")
        if not run_choice(ans):
            break

if __name__ == "__main__":
    main()
