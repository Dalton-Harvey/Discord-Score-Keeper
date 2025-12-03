
def scores_to_string(scores:dict) -> str:
    lines = []
    
    for user_id, data in scores.items():
        lines.append(f"{data['name']}: {data['score']}")        
        print(lines)

    return ", ".join(lines)
