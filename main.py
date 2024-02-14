# imports
from fastapi import FastAPI
from fastapi import (
    HTTPException,
    FastAPI,
    Depends,
)
from typing import Annotated
from passlib.hash import argon2
from mysql import connector
from utils.jwt import create_jwt
from utils.rbac import verify_admin, verify_driver, verify_student
from db.connect import get_db

# Documentation Code
description = """
The Drivertracking API helps the parents to track the location of their students bus route. The API is designed to be used by three types of users: parents, drivers, and admins.

The API uses **Json Web Tokens** for authentication and has **role based authorization**. 
"""

app = FastAPI(
    title="Driver Tracker API",
    version="1.0",
    description=description,
    openapi_tags=[
        {"name": "Authentication"},
        {"name": "Parents API"},
        {"name": "Driver API"},
        {"name": "Admin Bus Route API"},
        {"name": "Admin Bus Stand API"},
        {"name": "Admin Student API"},
        {"name": "Admin Driver API"},
    ],
)


# Classes to pass data from the functions to the controllers
StudentId = Annotated[str, Depends(verify_student)]
DriverId = Annotated[str, Depends(verify_driver)]


# PARENT API
@app.post("/student/login", tags=["Authentication"])
async def student_login(username: str, password: str):
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute(
            f"SELECT id,password FROM student WHERE username = '{username}';"
        )
        result = cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="User not found")
        if not argon2.verify(password, result[1]):
            raise HTTPException(status_code=401, detail="Invalid password")
        token = create_jwt({"id": result[0], "role": "student"})
        return {"message": token}
    except HTTPException as e:
        print(e)
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if db.is_connected():
            db.close()


@app.get(
    "/student/bus_route", dependencies=[Depends(verify_student)], tags=["Parents API"]
)
async def get_student_bus_route(id: StudentId):
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute(f"SELECT bus_route FROM student WHERE id = '{id}';")
        result = cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Student not found")
        return {"bus_route": result[0]}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if db.is_connected():
            db.close()


# DRIVER API
@app.post("/driver/login", tags=["Authentication"])
async def driver_login(username: str, password: str):
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM driver WHERE username = '{username}';")
        result = cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="User not found")
        if not argon2.verify(password, result[2]):
            raise HTTPException(status_code=401, detail="Invalid password")
        token = create_jwt({"id": result[0], "username": username, "role": "driver"})
        return {"message": token}
    except HTTPException as e:
        print(e)
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if db.is_connected():
            db.close()


@app.get(
    "/driver/bus_route", dependencies=[Depends(verify_driver)], tags=["Driver API"]
)
async def get_driver_bus_route(username_id: DriverId):
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM bus_route WHERE driver = '{username_id}';")
        result = cursor.fetchone()
        return {"bus_route": result}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if db.is_connected():
            db.close()


@app.put(
    "/driver/bus_route/location",
    dependencies=[Depends(verify_driver)],
    tags=["Driver API"],
)
async def update_driver_bus_route_location(id: DriverId, x: float, y: float):
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute(
            f"UPDATE bus_route SET location_x = {x}, location_y = {y}, last_location_updated = NOW() WHERE driver = '{id}';"
        )
        db.commit()
        return {"message": "Bus route location updated"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if db.is_connected():
            db.close()


@app.put(
    "/driver/bus_route/next_stop",
    dependencies=[Depends(verify_driver)],
    tags=["Driver API"],
)
async def update_driver_bus_route_next_stop(id: DriverId, next_stop: str):
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute(
            f"UPDATE bus_route SET next_stop = '{next_stop}' WHERE driver = '{id}';"
        )
        db.commit()
        return {"message": "Bus route next stop updated"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if db.is_connected():
            db.close()


# ADMIN API
@app.post("/admin/login", tags=["Authentication"])
async def admin_login(username: str, password: str):
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute(f"SELECT id,password FROM admin WHERE username = '{username}';")
        result = cursor.fetchone()
        print(result)
        if result is None:
            raise HTTPException(status_code=404, detail="User not found")
        if not argon2.verify(password, result[1]):
            raise HTTPException(status_code=401, detail="Invalid password")
        token = create_jwt({"id": result[0], "username": username, "role": "admin"})
        return {"message": token}
    except HTTPException as e:
        print(e)
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if db.is_connected():
            db.close()


# CRUD for Bus Route
@app.get(
    "/admin/bus_route",
    dependencies=[Depends(verify_admin)],
    tags=["Admin Bus Route API"],
)
async def get_all_bus_routes():
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM bus_route;")
        result = cursor.fetchall()
        return {"bus_routes": result}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if db.is_connected():
            db.close()


@app.get(
    "/admin/bus_route/{bus_route_id}/students",
    dependencies=[Depends(verify_admin)],
    tags=["Admin Bus Route API"],
)
async def get_students_for_bus_route(bus_route_id: str):
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM student WHERE bus_route = '{bus_route_id}';")
        result = cursor.fetchall()
        return {"students": result}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if db.is_connected():
            db.close()


@app.get(
    "/admin/bus_route/{id}",
    dependencies=[Depends(verify_admin)],
    tags=["Admin Bus Route API"],
)
async def get_bus_route_by_id(id: str):
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM bus_route WHERE id = '{id}';")
        result = cursor.fetchone()
        return {"bus_route": result}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if db.is_connected():
            db.close()


@app.post(
    "/admin/bus_route",
    dependencies=[Depends(verify_admin)],
    tags=["Admin Bus Route API"],
)
async def create_bus_route(name: str):
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute(
            f"INSERT INTO bus_route (name, last_location_updated) VALUES ('{name}', NOW());"
        )
        db.commit()

        cursor.execute(f"SELECT * FROM bus_route WHERE name = '{name}';")
        res = cursor.fetchone()
        return {"message": f"Bus route created, with id {res[0]}"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if db.is_connected():
            db.close()


@app.put(
    "/admin/bus_route/{id}",
    dependencies=[Depends(verify_admin)],
    tags=["Admin Bus Route API"],
)
async def update_bus_route(id: str, location_x: float, location_y: float):
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute(
            f"UPDATE bus_route SET location_x = {location_x}, location_y = {location_y}, last_location_updated = NOW() WHERE id = '{id}';"
        )
        db.commit()
        return {"message": "Bus route updated"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if db.is_connected():
            db.close()


@app.delete(
    "/admin/bus_route/{id}",
    dependencies=[Depends(verify_admin)],
    tags=["Admin Bus Route API"],
)
async def delete_bus_route(id: str):
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute(f"DELETE FROM bus_route WHERE id = '{id}';")
        db.commit()
        return {"message": "Bus route deleted"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if db.is_connected():
            db.close()


@app.get(
    "/admin/bus_route/{id}/bus_stands",
    dependencies=[Depends(verify_admin)],
    tags=["Admin Bus Route API"],
)
async def get_bus_stands_for_route(id: str):
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute(
            f"SELECT * FROM bus_stand WHERE bus_route = '{id}' ORDER BY route_order;"
        )
        result = cursor.fetchall()
        return {"bus_stands": result}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if db.is_connected():
            db.close()


# CRUD for Bus Stand
@app.get(
    "/admin/bus_stand/{id}",
    dependencies=[Depends(verify_admin)],
    tags=["Admin Bus Stand API"],
)
async def get_bus_stand_by_id(id: str):
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM bus_stand WHERE id = '{id}';")
        result = cursor.fetchone()
        return {"bus_stand": result}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if db.is_connected():
            db.close()


@app.post(
    "/admin/bus_stand",
    dependencies=[Depends(verify_admin)],
    tags=["Admin Bus Stand API"],
)
async def create_bus_stand(
    name: str,
    x_coordinate: float,
    y_coordinate: float,
    bus_route: str,
    route_order: int,
):
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute(
            f"INSERT INTO bus_stand (name, x_coordinate, y_coordinate, bus_route, route_order) VALUES ('{name}', {x_coordinate}, {y_coordinate}, '{bus_route}', {route_order});"
        )
        db.commit()
        return {"message": "Bus stand created"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if db.is_connected():
            db.close()


@app.put(
    "/admin/bus_stand/{id}",
    dependencies=[Depends(verify_admin)],
    tags=["Admin Bus Stand API"],
)
async def update_bus_stand(
    id: str,
    name: str,
    x_coordinate: float,
    y_coordinate: float,
    bus_route: str,
    route_order: int,
):
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute(
            f"UPDATE bus_stand SET name = '{name}', x_coordinate = {x_coordinate}, y_coordinate = {y_coordinate}, bus_route = '{bus_route}', route_order = {route_order} WHERE id = '{id}';"
        )
        db.commit()
        return {"message": "Bus stand updated"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if db.is_connected():
            db.close()


@app.delete(
    "/admin/bus_stand/{id}",
    dependencies=[Depends(verify_admin)],
    tags=["Admin Bus Stand API"],
)
async def delete_bus_stand(id: str):
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute(f"DELETE FROM bus_stand WHERE id = '{id}';")
        db.commit()
        return {"message": "Bus stand deleted"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if db.is_connected():
            db.close()


# CRUD for Student
@app.get(
    "/admin/student", dependencies=[Depends(verify_admin)], tags=["Admin Student API"]
)
async def get_all_students():
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM student;")
        result = cursor.fetchall()
        return {"students": result}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if db.is_connected():
            db.close()


@app.get(
    "/admin/student/{id}",
    dependencies=[Depends(verify_admin)],
    tags=["Admin Student API"],
)
async def get_student_by_id(id: str):
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM student WHERE id = '{id}';")
        result = cursor.fetchone()
        return {"student": result}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if db.is_connected():
            db.close()


@app.post(
    "/admin/student", dependencies=[Depends(verify_admin)], tags=["Admin Student API"]
)
async def add_student(name: str, username: str, bus_route: str):
    db = get_db()

    # Generate a random password
    def generate_password():
        import random
        import string

        return "".join(
            random.choice(string.ascii_letters + string.digits) for i in range(8)
        )

    password = generate_password()
    hashed_password = argon2.hash(password)
    try:
        cursor = db.cursor()
        cursor.execute(
            f"INSERT INTO student (name, username, bus_route, password) VALUES ('{id}', '{name}', '{username}', '{bus_route}', '{hashed_password}');"
        )
        db.commit()
        msg = f"Student added, the password is {password}"
        return {"message": msg}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if db.is_connected():
            db.close()


@app.put(
    "/admin/student/{id}",
    dependencies=[Depends(verify_admin)],
    tags=["Admin Student API"],
)
async def update_student(id: str, username: str, name: str, bus_route: str):
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute(
            f"UPDATE student SET name = '{name}', bus_route = '{bus_route}', username = '{username}' WHERE id = '{id}';"
        )
        db.commit()
        return {"message": "Student updated"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if db.is_connected():
            db.close()


@app.delete(
    "/admin/student/{id}",
    dependencies=[Depends(verify_admin)],
    tags=["Admin Student API"],
)
async def remove_student(id: str):
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute(f"DELETE FROM student WHERE id = '{id}';")
        db.commit()
        return {"message": "Student removed"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if db.is_connected():
            db.close()


# CRUD for Driver
@app.get(
    "/admin/driver", dependencies=[Depends(verify_admin)], tags=["Admin Driver API"]
)
async def get_all_drivers():
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM driver;")
        result = cursor.fetchall()
        return {"drivers": result}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if db.is_connected():
            db.close()


@app.get(
    "/admin/driver/{id}",
    dependencies=[Depends(verify_admin)],
    tags=["Admin Driver API"],
)
async def get_driver_by_id(id: str):
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM driver WHERE id = '{id}';")
        result = cursor.fetchone()
        return {"driver": result}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if db.is_connected():
            db.close()


@app.post(
    "/admin/driver", dependencies=[Depends(verify_admin)], tags=["Admin Driver API"]
)
async def add_driver(username: str, name: str, bus_route: str):
    db = get_db()

    # Generate a random password
    def generate_password():
        import random
        import string

        return "".join(
            random.choice(string.ascii_letters + string.digits) for i in range(8)
        )

    password = generate_password()
    hashed_password = argon2.hash(password)
    try:
        cursor = db.cursor()
        cursor.execute(
            f"INSERT INTO driver (username, name, password) VALUES ('{username}', '{name}', '{hashed_password}');"
        )
        db.commit()

        cursor.execute(f"SELECT * FROM driver WHERE username = '{username}';")
        drv = cursor.fetchone()

        cursor.execute(
            f"UPDATE bus_route SET driver = '{drv[0]}' WHERE id = '{bus_route}';"
        )
        db.commit()

        return {"message": f"Driver added, the password is {password}"}
    except connector.errors.Error as e:
        print(e)
        if e.errno == 1062:
            raise HTTPException(status_code=422, detail="Value already exists")
        else:
            raise HTTPException(status_code=422, detail="Internal Server Error")
    except Exception as e:
        print(e)
        cursor.execute(f"DELETE FROM driver WHERE username = '{username}';")
        db.commit()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if db.is_connected():
            db.close()


@app.put(
    "/admin/driver/{id}",
    dependencies=[Depends(verify_admin)],
    tags=["Admin Driver API"],
)
async def update_driver(id: str, username: str, name: str, bus_route: str):
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute(
            f"UPDATE driver SET name = '{name}', username ='{username}' WHERE id = '{id}';"
        )
        db.commit()

        cursor.execute(f"SELECT * FROM driver WHERE id = '{id}';")
        drv = cursor.fetchone()

        cursor.execute(f"UPDATE bus_route SET driver = null WHERE id = '{drv[0]}';")
        cursor.execute(
            f"UPDATE bus_route SET driver = '{id}' WHERE id = '{bus_route}';"
        )
        return {"message": "Driver updated"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if db.is_connected():
            db.close()


@app.delete(
    "/admin/driver/{id}",
    dependencies=[Depends(verify_admin)],
    tags=["Admin Driver API"],
)
async def remove_driver(id: str):
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute(f"DELETE FROM driver WHERE id = '{id}';")
        db.commit()
        return {"message": "Driver removed"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if db.is_connected():
            db.close()
