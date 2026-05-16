#Test para la clase User.
from entities.user import User
from enums.profile import Profile

print("=== TEST 1: Guardar usuario jugador ===")
saved = User.save("Juan", "juan@test.com", "123456", Profile.PLAYER)
print("Resultado:", saved)  # True

print("\n=== TEST 2: Guardar usuario admin ===")
saved_admin = User.save("Admin", "admin@test.com", "admin123", Profile.ADMIN)
print("Resultado:", saved_admin)  # True

print("\n=== TEST 3: Login correcto ===")
user = User.check_login("juan@test.com", "123456")
print("Usuario:", user.name if user else "FALLÓ")  # Juan

print("\n=== TEST 4: Login con contraseña incorrecta ===")
user_fail = User.check_login("juan@test.com", "wrongpass")
print("Resultado:", user_fail)  # None

print("\n=== TEST 5: Login con email inexistente ===")
user_fail2 = User.check_login("noexiste@test.com", "123456")
print("Resultado:", user_fail2)  # None

print("\n=== TEST 6: Get by ID ===")
user_by_id = User.get_by_id(1)
print("Usuario:", user_by_id.name if user_by_id else "No encontrado")  # Juan

print("\n=== TEST 7: Verificar is_admin ===")
admin = User.check_login("admin@test.com", "admin123")
print("Es admin:", admin.is_admin() if admin else "FALLÓ")   # True
print("Jugador es admin:", user.is_admin() if user else "FALLÓ")  # False

print("\n=== TEST 8: Verificar is_active ===")
user_active = User.get_by_id(1)
print("Is active:", user_active.is_active if user_active else "FALLÓ")  # True
