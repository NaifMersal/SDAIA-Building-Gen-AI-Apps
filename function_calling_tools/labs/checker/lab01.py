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
        assert "enum" in props["price_range"], \
            "price_range should use 'enum' to constrain values"
        assert set(props["price_range"]["enum"]) == {"budget", "mid", "luxury"}, \
            "price_range enum should be: budget, mid, luxury"
        assert props["amenities"]["type"] == "array", \
            "amenities should be type 'array'"
        assert "items" in props["amenities"], \
            "amenities should have an 'items' definition"
        assert "enum" in props["amenities"]["items"], \
            "amenities items should use 'enum' to constrain allowed values"
        required = schema["function"]["parameters"].get("required", [])
        assert "location" in required and "price_range" in required, \
            "Both 'location' and 'price_range' should be required"
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
        assert "city" in schema["properties"], "Missing 'city' field"
        assert "price_per_night" in schema["properties"], "Missing 'price_per_night' field"
        assert "rating" in schema["properties"], "Missing 'rating' field"
        assert "amenities" in schema["properties"], "Missing 'amenities' field"

        # Negative price should be rejected
        try:
            model_class(name="Test", city="Riyadh", price_per_night=-50, rating=3.0, amenities=[])
            print("❌ Error: Model should have rejected negative price!")
            return False
        except ValidationError:
            pass

        # Rating > 5.0 should be rejected
        try:
            model_class(name="Test", city="Riyadh", price_per_night=100, rating=6.0, amenities=[])
            print("❌ Error: Model should have rejected rating > 5.0!")
            return False
        except ValidationError:
            pass

        # A valid instance should parse correctly
        instance = model_class(
            name="Grand Palace", city="Riyadh",
            price_per_night=350.0, rating=4.5, amenities=["wifi", "pool"]
        )
        assert instance.name == "Grand Palace"

        print("✅ Part 2: Hotel Model check passed!")
        return True
    except AssertionError as e:
        print(f"❌ Part 2 Check Failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Part 2 Check Error: {e}")
        return False


def check_calculator_logic(execute_func):
    """Validates the execute_calculation function (4 core operations)."""
    try:
        # Basic arithmetic
        assert execute_func("add", 10, 5)["result"] == 15, \
            "add: 10 + 5 should equal 15"
        assert execute_func("subtract", 10, 3)["result"] == 7, \
            "subtract: 10 - 3 should equal 7"
        assert execute_func("multiply", 500, 0.15)["result"] == 75.0, \
            "multiply: 500 * 0.15 should equal 75.0"
        assert execute_func("divide", 10, 2)["result"] == 5.0, \
            "divide: 10 / 2 should equal 5.0"

        # Division by zero must return success=False, NOT raise an exception
        div_zero = execute_func("divide", 10, 0)
        assert div_zero["success"] == False, \
            "divide by zero should return {'success': False, ...}"
        assert div_zero["error"] is not None, \
            "divide by zero should include an error message"

        # Unknown operation must return success=False, NOT raise
        unknown = execute_func("sqrt", 9, 0)
        assert unknown["success"] == False, \
            "unsupported operation should return {'success': False, ...}"

        print("✅ Part 3: Calculator Logic check passed!")
        return True
    except AssertionError as e:
        print(f"❌ Part 3 Check Failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Part 3 Check Error: {e}")
        return False
