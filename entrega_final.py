import sqlite3
from datetime import datetime

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm


console = Console()
DB_NAME = "inventario.db"


# -----------------------------
# BASE DE DATOS
# -----------------------------
def conectar():
    return sqlite3.connect(DB_NAME)

def cargar_datos_iniciales():
    productos_iniciales = [
        {
            "codigo": "AA0054",
            "nombre": "Arroz",
            "descripcion": "Producto de almacén",
            "categoria": "Almacén",
            "precio": 123,
            "cantidad": 3
        },
        {
            "codigo": "CC5689",
            "nombre": "Cacao",
            "descripcion": "Producto de almacén",
            "categoria": "Almacén",
            "precio": 456,
            "cantidad": 5
        },
        {
            "codigo": "TT3245",
            "nombre": "Té",
            "descripcion": "Producto de almacén",
            "categoria": "Almacén",
            "precio": 789,
            "cantidad": 30
        }
    ]

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT COUNT(*) FROM productos")
    cantidad_productos = cursor.fetchone()[0]

    if cantidad_productos == 0:
        fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for producto in productos_iniciales:
            cursor.execute("""
                INSERT INTO productos 
                (codigo, nombre, descripcion, cantidad, precio, categoria, fecha_registro)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                producto["codigo"],
                producto["nombre"],
                producto["descripcion"],
                producto["cantidad"],
                producto["precio"],
                producto["categoria"],
                fecha_registro
            ))

        conexion.commit()

    conexion.close()

def crear_tabla():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         codigo TEXT,
         nombre TEXT NOT NULL,
         descripcion TEXT,
         cantidad INTEGER NOT NULL,
         precio REAL NOT NULL,
         categoria TEXT,
         fecha_registro TEXT NOT NULL  
        )
    """)

    conexion.commit()
    conexion.close()


# -----------------------------
# VALIDACIONES
# -----------------------------
def pedir_texto_obligatorio(mensaje):
    while True:
        valor = Prompt.ask(mensaje).strip()

        if valor != "":
            return valor

        console.print("[red]El campo no puede estar vacío.[/red]")


def pedir_entero_no_negativo(mensaje):
    while True:
        valor = Prompt.ask(mensaje).strip()

        if valor.isdigit():
            return int(valor)

        console.print("[red]Tenés que ingresar un número entero válido.[/red]")


def pedir_precio(mensaje):
    while True:
        valor = Prompt.ask(mensaje).strip()

        try:
            precio = float(valor)

            if precio >= 0:
                return precio

            console.print("[red]El precio no puede ser negativo.[/red]")

        except ValueError:
            console.print("[red]Tenés que ingresar un precio válido. Ejemplo: 1500 o 1500.50[/red]")


def pausar():
    input("\nPresioná ENTER para continuar...")


# -----------------------------
# FUNCIONES DEL SISTEMA
# -----------------------------
def agregar_producto():
    console.print(Panel("[bold cyan]Registrar nuevo producto[/bold cyan]"))

    nombre = pedir_texto_obligatorio("Nombre del producto")
    descripcion = Prompt.ask("Descripción breve", default="Sin descripción").strip()
    cantidad = pedir_entero_no_negativo("Cantidad disponible")
    precio = pedir_precio("Precio del producto")
    categoria = Prompt.ask("Categoría", default="Sin categoría").strip()

    fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria, fecha_registro)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nombre, descripcion, cantidad, precio, categoria, fecha_registro))

    conexion.commit()
    conexion.close()

    console.print("[green]✅ Producto registrado correctamente.[/green]")


def visualizar_productos():
    console.print(Panel("[bold cyan]Productos registrados[/bold cyan]"))

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, nombre, descripcion, cantidad, precio, categoria, fecha_registro
        FROM productos
        ORDER BY id
    """)

    productos = cursor.fetchall()
    conexion.close()

    if not productos:
        console.print("[yellow]No hay productos registrados todavía.[/yellow]")
        return

    tabla = Table(title="Inventario de productos")

    tabla.add_column("ID", justify="center", style="cyan")
    tabla.add_column("Nombre", style="bold")
    tabla.add_column("Descripción")
    tabla.add_column("Cantidad", justify="center")
    tabla.add_column("Precio", justify="right")
    tabla.add_column("Categoría")
    tabla.add_column("Fecha registro")

    for producto in productos:
        tabla.add_row(
            str(producto[0]),
            producto[1],
            producto[2],
            str(producto[3]),
            f"${producto[4]:.2f}",
            producto[5],
            producto[6]
        )

    console.print(tabla)


def buscar_producto_por_id():
    console.print(Panel("[bold cyan]Buscar producto por ID[/bold cyan]"))

    id_producto = pedir_entero_no_negativo("ID del producto a buscar")

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, nombre, descripcion, cantidad, precio, categoria, fecha_registro
        FROM productos
        WHERE id = ?
    """, (id_producto,))

    producto = cursor.fetchone()
    conexion.close()

    if producto is None:
        console.print("[red]No existe un producto con ese ID.[/red]")
        return

    tabla = Table(title="Producto encontrado")

    tabla.add_column("Campo", style="cyan")
    tabla.add_column("Valor")

    tabla.add_row("ID", str(producto[0]))
    tabla.add_row("Nombre", producto[1])
    tabla.add_row("Descripción", producto[2])
    tabla.add_row("Cantidad", str(producto[3]))
    tabla.add_row("Precio", f"${producto[4]:.2f}")
    tabla.add_row("Categoría", producto[5])
    tabla.add_row("Fecha registro", producto[6])

    console.print(tabla)


def buscar_producto():
    console.print(Panel("[bold cyan]Buscar producto[/bold cyan]"))

    console.print("1 - Buscar por ID")
    console.print("2 - Buscar por nombre")
    console.print("3 - Buscar por categoría")

    opcion = Prompt.ask("Elegí una opción", choices=["1", "2", "3"])

    conexion = conectar()
    cursor = conexion.cursor()

    match opcion:
        case "1":
            id_producto = pedir_entero_no_negativo("ID del producto")

            cursor.execute("""
                SELECT id, nombre, descripcion, cantidad, precio, categoria, fecha_registro
                FROM productos
                WHERE id = ?
            """, (id_producto,))

        case "2":
            nombre = pedir_texto_obligatorio("Nombre o parte del nombre")

            cursor.execute("""
                SELECT id, nombre, descripcion, cantidad, precio, categoria, fecha_registro
                FROM productos
                WHERE nombre LIKE ?
            """, (f"%{nombre}%",))

        case "3":
            categoria = pedir_texto_obligatorio("Categoría o parte de la categoría")

            cursor.execute("""
                SELECT id, nombre, descripcion, cantidad, precio, categoria, fecha_registro
                FROM productos
                WHERE categoria LIKE ?
            """, (f"%{categoria}%",))

        case _:
            console.print("[red]Opción inválida.[/red]")
            conexion.close()
            return

    productos = cursor.fetchall()
    conexion.close()

    if not productos:
        console.print("[red]No se encontraron productos.[/red]")
        return

    tabla = Table(title="Resultado de búsqueda")

    tabla.add_column("ID", justify="center", style="cyan")
    tabla.add_column("Nombre", style="bold")
    tabla.add_column("Descripción")
    tabla.add_column("Cantidad", justify="center")
    tabla.add_column("Precio", justify="right")
    tabla.add_column("Categoría")
    tabla.add_column("Fecha registro")

    for producto in productos:
        tabla.add_row(
            str(producto[0]),
            producto[1],
            producto[2],
            str(producto[3]),
            f"${producto[4]:.2f}",
            producto[5],
            producto[6]
        )

    console.print(tabla)


def actualizar_producto():
    console.print(Panel("[bold cyan]Actualizar producto[/bold cyan]"))

    id_producto = pedir_entero_no_negativo("ID del producto a actualizar")

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, nombre, descripcion, cantidad, precio, categoria
        FROM productos
        WHERE id = ?
    """, (id_producto,))

    producto = cursor.fetchone()

    if producto is None:
        conexion.close()
        console.print("[red]No existe un producto con ese ID.[/red]")
        return

    console.print("[yellow]Dejá vacío un campo si querés mantener el dato actual.[/yellow]")

    nuevo_nombre = Prompt.ask(f"Nombre actual: {producto[1]}", default="").strip()
    nueva_descripcion = Prompt.ask(f"Descripción actual: {producto[2]}", default="").strip()
    nueva_cantidad = Prompt.ask(f"Cantidad actual: {producto[3]}", default="").strip()
    nuevo_precio = Prompt.ask(f"Precio actual: {producto[4]}", default="").strip()
    nueva_categoria = Prompt.ask(f"Categoría actual: {producto[5]}", default="").strip()

    if nuevo_nombre == "":
        nuevo_nombre = producto[1]

    if nueva_descripcion == "":
        nueva_descripcion = producto[2]

    if nueva_categoria == "":
        nueva_categoria = producto[5]

    if nueva_cantidad == "":
        nueva_cantidad = producto[3]
    else:
        while not nueva_cantidad.isdigit():
            console.print("[red]La cantidad debe ser un número entero.[/red]")
            nueva_cantidad = Prompt.ask("Nueva cantidad").strip()
        nueva_cantidad = int(nueva_cantidad)

    if nuevo_precio == "":
        nuevo_precio = producto[4]
    else:
        while True:
            try:
                nuevo_precio = float(nuevo_precio)
                break
            except ValueError:
                console.print("[red]El precio debe ser un número válido.[/red]")
                nuevo_precio = Prompt.ask("Nuevo precio").strip()

    cursor.execute("""
        UPDATE productos
        SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ?
        WHERE id = ?
    """, (nuevo_nombre, nueva_descripcion, nueva_cantidad, nuevo_precio, nueva_categoria, id_producto))

    conexion.commit()
    conexion.close()

    console.print("[green]✅ Producto actualizado correctamente.[/green]")


def eliminar_producto():
    console.print(Panel("[bold cyan]Eliminar producto[/bold cyan]"))

    id_producto = pedir_entero_no_negativo("ID del producto a eliminar")

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, nombre, descripcion, cantidad, precio, categoria
        FROM productos
        WHERE id = ?
    """, (id_producto,))

    producto = cursor.fetchone()

    if producto is None:
        conexion.close()
        console.print("[red]No existe un producto con ese ID.[/red]")
        return

    console.print(f"[yellow]Producto encontrado: {producto[1]} - Stock: {producto[3]} - Precio: ${producto[4]:.2f}[/yellow]")

    confirmar = Confirm.ask("¿Seguro que querés eliminar este producto?")

    if confirmar:
        cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
        conexion.commit()
        console.print("[green]✅ Producto eliminado correctamente.[/green]")
    else:
        console.print("[yellow]Operación cancelada.[/yellow]")

    conexion.close()


def reporte_bajo_stock():
    console.print(Panel("[bold cyan]Reporte de productos con bajo stock[/bold cyan]"))

    limite = pedir_entero_no_negativo("Mostrar productos con cantidad igual o inferior a")

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, nombre, descripcion, cantidad, precio, categoria, fecha_registro
        FROM productos
        WHERE cantidad <= ?
        ORDER BY cantidad ASC
    """, (limite,))

    productos = cursor.fetchall()
    conexion.close()

    fecha_reporte = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    console.print(f"[dim]Fecha del reporte: {fecha_reporte}[/dim]")

    if not productos:
        console.print("[green]No hay productos con bajo stock según ese límite.[/green]")
        return

    tabla = Table(title=f"Productos con stock igual o inferior a {limite}")

    tabla.add_column("ID", justify="center", style="cyan")
    tabla.add_column("Nombre", style="bold")
    tabla.add_column("Cantidad", justify="center", style="red")
    tabla.add_column("Precio", justify="right")
    tabla.add_column("Categoría")

    for producto in productos:
        tabla.add_row(
            str(producto[0]),
            producto[1],
            str(producto[3]),
            f"${producto[4]:.2f}",
            producto[5]
        )

    console.print(tabla)


# -----------------------------
# MENÚ PRINCIPAL
# -----------------------------
def mostrar_menu():
    console.print(Panel.fit(
        "[bold cyan]Sistema de Gestión de Inventario[/bold cyan]\n"
        "[dim]Trabajo práctico final - Python + SQLite + Rich[/dim]",
        border_style="cyan"
    ))

    console.print("[bold]1[/bold] - Registrar nuevo producto")
    console.print("[bold]2[/bold] - Visualizar productos")
    console.print("[bold]3[/bold] - Actualizar producto por ID")
    console.print("[bold]4[/bold] - Eliminar producto por ID")
    console.print("[bold]5[/bold] - Buscar producto")
    console.print("[bold]6[/bold] - Reporte de bajo stock")
    console.print("[bold]7[/bold] - Salir")


def menu():
    crear_tabla()
    cargar_datos_iniciales()

    while True:
        console.clear()
        mostrar_menu()

        opcion = Prompt.ask("Elegí una opción", choices=["1", "2", "3", "4", "5", "6", "7"])

        console.clear()

        match opcion:
            case "1":
                agregar_producto()
                pausar()

            case "2":
                visualizar_productos()
                pausar()

            case "3":
                actualizar_producto()
                pausar()

            case "4":
                eliminar_producto()
                pausar()

            case "5":
                buscar_producto()
                pausar()

            case "6":
                reporte_bajo_stock()
                pausar()

            case "7":
                console.print("[green]Gracias por usar el sistema de gestión de inventario.[/green]")
                break

            case _:
                console.print("[red]Opción inválida.[/red]")
                pausar()

if __name__ == "__main__":
    menu()