from PIL import Image, ImageDraw

def draw_path(image_path, node_map, path, output_path="data/result.png"):
    img = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(img)
    coords = [(node_map[n]["x"], node_map[n]["y"]) for n in path]
    
    # Draw thick blue path line
    if len(coords) >= 2:
        # Draw multiple times for thickness
        for offset in range(-4, 5):
            shifted = [(x+offset, y) for x, y in coords]
            draw.line(shifted, fill=(0, 120, 255), width=1)
        for offset in range(-4, 5):
            shifted = [(x, y+offset) for x, y in coords]
            draw.line(shifted, fill=(0, 120, 255), width=1)
        draw.line(coords, fill=(0, 120, 255), width=8)

    # Draw dots on each node
    for i, nid in enumerate(path):
        x, y = node_map[nid]["x"], node_map[nid]["y"]
        label = node_map[nid]["label"]
        is_waypoint = any(k in label for k in ["Door", "Hallway", "Corridor"])

        if is_waypoint:
            # Small gray dot for corridor waypoints
            draw.ellipse([x-6, y-6, x+6, y+6], fill=(150, 150, 150))
        else:
            # Big colored dot for rooms
            color = (0, 200, 0) if i == 0 else (255, 50, 50)
            draw.ellipse([x-20, y-20, x+20, y+20], fill=color, outline="white", width=3)
            # Label background
            tw = len(label) * 10
            draw.rectangle([x+22, y-16, x+22+tw, y+12], fill="white", outline=color, width=2)
            draw.text((x+25, y-13), label, fill=color)

    img.save(output_path)
    return output_path
    