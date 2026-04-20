from pprint import pprint

class QueryGenerator:
    
    @staticmethod
    def generate_expr(compare_option, value1, value2):
        return_expr =  {
                    "$expr": {
                        f"${compare_option}": [value1, value2]
                    }   
                }
        
        return return_expr
    
    
    @staticmethod
    def generate_and(condition_list):
        
        return_and = {}

        if condition_list:
            return_and = {"$and": condition_list}
        
        return return_and
    
    @staticmethod
    def generate_match(match_: dict):
        if not match_:
            return {}

        return_match = {
            "$match": match_
        }

        return return_match
    
    @staticmethod
    def generate_lookup(from_, local_field, foreign_field, as_):
        return_lookup =  {
            "$lookup": {
                "from": from_,
                "localField": local_field,
                "foreignField": foreign_field,
                "as": as_
            }
        }

        return return_lookup
    
    @staticmethod
    def generate_lookup_with_pipeline(from_: str, local_field: str, foreign_field: str, as_: str, nested_lookup: dict = None, unwind: str = None):

        let_variable_name = f"to_{from_}_lookup_id"

        pipeline = [QueryGenerator.generate_match(QueryGenerator.generate_expr("eq", f"$${let_variable_name}", f"${foreign_field}"))]

        if nested_lookup:
            pipeline.append(nested_lookup)

        return_lookup =  {
            "$lookup": {
                "from": from_,
                "let": {let_variable_name: f"${local_field}"},
                "pipeline": pipeline,
                "as": as_
            }
        }

        if unwind:
            pipeline.append(QueryGenerator.generate_unwind(unwind))
        
        return return_lookup

    @staticmethod
    def generate_project(project_: dict):
        if not project_:
            return {}
        
        return_project = {
            "$project": project_
        }
       
        return return_project
    

    @staticmethod
    def generate_unwind(unwind_: str):
        if not unwind_:
            return {}
        
        return_limit = {
            "$unwind": f"${unwind_}"
        }

        return return_limit
    
    @staticmethod
    def generate_sort(sort_: dict):
        if not sort_:
            return {}
        
        return_sort = {
            "$sort": sort_
        }

        return return_sort
    
    @staticmethod
    def generate_limit(limit_: int):
        return_limit = {
            "$limit": limit_
        }

        return return_limit
    
    @staticmethod
    def generate_map(input: str, as_: str, in_: str):
        return_map = {
            "$map": {
                "input": f"${input}",
                "as": as_,
                "in": f"$${as_}.{in_}"
            }
        }

        return return_map
    
    @staticmethod
    def generate_add_fields(add_fields: dict):
        
        if not add_fields:
            return {} 
        
        return_add_fields = {
            "$addFields": add_fields
        }

        return return_add_fields
    
    @staticmethod
    def generate_simple_switch(field_check, compare_option, check_logic: dict, default):
        
        if not check_logic:
            return {} 
        
        branches = []

        for check_value, result in check_logic.items():
            case_ = { "case": {f"${compare_option}": [f"${field_check}", check_value] }, "then": result}
            branches.append(case_)
            
        return_switch = {
                "$switch": {
                    "branches": branches,
                    "default": default
                }
            }

        return return_switch
    
    


