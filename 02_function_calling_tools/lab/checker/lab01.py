import json
from pydantic import ValidationError

def check_hotel_schema(schema):
    """Validates the search_hotels_schema designed by the student."""
    try:
        assert schema["function"]["name"] == "search_hotels"
        props = schema["function"]["parameters"]["properties"]
        assert "location" in props, "Missing 'location' property"
        assert "price_range" in props, "Missing 'price_range' property"
        assert "amenities" in props, "Missing 'amenities' property"
        assert "enum" in props["price_range"], "price_range should use enum"
        assert props["amenities"]["type"] == "array", "amenities should be an array"
        print("✅ Part 1: Hotel Schema check passed!")
        return True
    except AssertionError as e:
        print(f"❌ Part 1 Check Failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Part 1 Check Error: {e}")
        return False

def check_hotel_model(model_class):
    """Validates the HotelResult Pydantic model."""
    try:
        schema = model_class.model_json_schema()
        assert "name" in schema["properties"], "Missing 'name' field"
        assert "price_per_night" in schema["properties"], "Missing 'price_per_night' field"
        assert "rating" in schema["properties"], "Missing 'rating' field"

        # Test validation works
        try:
            model_class(name="Test", city="Riyadh", price_per_night=-50, rating=3.0, amenities=[])
            print("❌ Error: Model should have rejected negative price!")
            return False
        except ValidationError:
            pass
            
        print("✅ Part 2: Hotel Model check passed!")
        return True
    except AssertionError as e:
        print(f"❌ Part 2 Check Failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Part 2 Check Error: {e}")
        return False

def check_calculator_logic(execute_func):
    """Validates the execute_calculation function logic."""
    try:
        assert execute_func("add", 10, 5)["result"] == 15
        assert execute_func("multiply", 500, 0.15)["result"] == 75.0
        assert execute_func("divide", 10, 0)["success"] == False
        assert execute_func("pow", 2, 10)["result"] == 1024
        assert execute_func("sqrt", 9, 0)["success"] == False
        print("✅ Part 3: Calculator Logic check passed!")
        return True
    except AssertionError as e:
        print(f"❌ Part 3 Check Failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Part 3 Check Error: {e}")
        return False
