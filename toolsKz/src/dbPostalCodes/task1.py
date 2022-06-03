class StepTreeRoot: 

    def __init__(self) -> None:
        
        self.step_tree_json = { 
            "CurrentTrees": [ 
                { 
                    "RootSteps": [] 
                } 
            ] 
        } 

    def bind_step(self, step_name):

        print(step_name)

        adress = step_name.split(".")
        print(adress)

        pass

    def __enter__(self): 
        return self 

    def __exit__(self, exc_type, exc_value, exc_traceback): 
        print(self.step_tree_json) 

class Step:

    def __init__(self):

        self.step_format = { 
            "Childs": [], 
            "IsBreaking": "false", 
            "StepTitle": "", 
            "ExceptionMessage": "" 
        }

    def __enter__(self): 
        return self 

    def __exit__(self, exc_type, exc_value, exc_traceback): 
        # Параметры
        self.end() 

    def bind_step(self, step_name):

        print(step_name)

        print("in small step")
        pass

    def end(self): 
        # sdf
        pass


def main():

    try: 
        with StepTreeRoot() as step_tree: 
            with step_tree.bind_step("1") as step:
                with step.bind_step("1.1"): 
                    pass 

                with step.bind_step("1.2"): 
                        pass 

            with step_tree.bind_step("2") as step: 
                with step.bind_step("2.1"): 
                    pass 

            with step_tree.bind_step("3"): 
                raise Exception("Exception message") 
    except Exception as e:
        print(e) 


if __name__ == "__main__":

    main()
