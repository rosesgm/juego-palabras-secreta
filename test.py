from entities.level import Level


print("=== TEST 1: Guardar nivel ===")
saved = Level.save(1, "El Castor", "castor.png",
                   "Es un animal que construye presas", "castor")
print("Resultado:", saved)  # True

print("\n=== TEST 2: Obtener nivel por número ===")
level = Level.get_by_number(1)
print("Nivel:", level.title if level else "No encontrado")  # El Castor

print("\n=== TEST 3: Respuesta correcta ===")
print("Resultado:", level.check_answer("castor"))  # True

print("\n=== TEST 4: Respuesta con mayúsculas ===")
print("Resultado:", level.check_answer("Castor"))  # True

print("\n=== TEST 5: Respuesta incorrecta ===")
print("Resultado:", level.check_answer("perro"))  # False

print("\n=== TEST 6: Obtener todos los niveles ===")
levels = Level.get_all()
print("Total niveles:", len(levels))  # 1
