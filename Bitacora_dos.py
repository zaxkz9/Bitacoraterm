# Bitacora de tareas y recibos
# Estructuras de datos: lista enlazada, pila, cola y tabla hash
# Algoritmos: ordenamiento por merge sort, busqueda lineal y binaria y dispersion hash

from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation

class Nodo:
    def __init__(self, dato):       #definir la estructura de nodo como una clase
        self.dato = dato
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.inicio = None             #definir la lista enlazada
        self.fin = None
        self.tamano = 0

    def esta_vacia(self):                       #definir si la lista esta vacia 
        return self.inicio is None

    def __len__(self):
        return self.tamano

    def __iter__(self):
        actual = self.inicio
        while actual is not None:         #definicion de como un tipo de bucle, en caso de no encontrar un elemento pasa al siguiente y el siguiente se convierte en el actual
            yield actual.dato
            actual = actual.siguiente

    def agregar_al_final(self, dato):
        nuevo = Nodo(dato)
        if self.inicio is None:
            self.inicio = nuevo
        else:                                   #definicion para agregar un elemento al final, si no hay elemento sera el más nuevo/primero, y si ya hay elemento se va al final
            self.fin.siguiente = nuevo
        self.fin = nuevo
        self.tamano += 1
        return dato

    def eliminar(self, cumple):
        anterior = None
        actual = self.inicio
        while actual is not None:
            if cumple(actual.dato):
                if anterior is None:
                    self.inicio = actual.siguiente          #definicion de eliminacion de elementos
                else:
                    anterior.siguiente = actual.siguiente
                if actual is self.fin:
                    self.fin = anterior
                self.tamano -= 1
                return actual.dato
            anterior = actual
            actual = actual.siguiente
        return None

    def buscar(self, cumple):                               #busqueda lineal: revisa nodo por nodo hasta que uno cumpla
        return self._buscar(self.inicio, cumple)

    def _buscar(self, nodo, cumple):
        if nodo is None:
            return None
        if cumple(nodo.dato):                               #definicion de busqueda, si no encuentra el nodo, no encontro, si cumple mostrar el elemento
            return nodo.dato
        return self._buscar(nodo.siguiente, cumple)

    def contar(self, cumple=None):
        return self._contar(self.inicio, cumple)

    def _contar(self, nodo, cumple):
        if nodo is None:
            return 0
        este = 1 if (cumple is None or cumple(nodo.dato)) else 0        
        return este + self._contar(nodo.siguiente, cumple)

    def filtrar(self, cumple):
        resultado = ListaEnlazada()
        self._filtrar(self.inicio, cumple, resultado)
        return resultado

    def _filtrar(self, nodo, cumple, resultado):
        if nodo is None:
            return
        if cumple(nodo.dato):
            resultado.agregar_al_final(nodo.dato)                   
        self._filtrar(nodo.siguiente, cumple, resultado)

    def copia(self):
        nueva = ListaEnlazada()
        for dato in self:
            nueva.agregar_al_final(dato)
        return nueva

    def a_arreglo(self):
        arreglo = []
        for dato in self:                   #pasar la lista enlazada a un arreglo indexable, la busqueda binaria necesita poder saltar a la mitad
            arreglo.append(dato)
        return arreglo

    def ordenar_por(self, clave):                           #ordenamiento: merge sort sobre la lista enlazada
        self.inicio = self._merge_sort(self.inicio, clave)
        self.fin = self._ultimo(self.inicio)

    def _merge_sort(self, cabeza, clave):
        if cabeza is None or cabeza.siguiente is None:
            return cabeza
        segunda = self._cortar_a_la_mitad(cabeza)
        izquierda = self._merge_sort(cabeza, clave)
        derecha = self._merge_sort(segunda, clave)
        return self._mezclar(izquierda, derecha, clave)

    def _cortar_a_la_mitad(self, cabeza):
        lento = cabeza
        rapido = cabeza.siguiente
        while rapido is not None and rapido.siguiente is not None:
            lento = lento.siguiente
            rapido = rapido.siguiente.siguiente
        segunda_mitad = lento.siguiente
        lento.siguiente = None
        return segunda_mitad

    def _mezclar(self, a, b, clave):
        if a is None:
            return b
        if b is None:
            return a
        if clave(a.dato) <= clave(b.dato):
            a.siguiente = self._mezclar(a.siguiente, b, clave)
            return a
        b.siguiente = self._mezclar(a, b.siguiente, clave)
        return b

    def _ultimo(self, nodo):
        if nodo is None:
            return None
        while nodo.siguiente is not None:
            nodo = nodo.siguiente
        return nodo


class Pila:
    def __init__(self):         #clase de pila
        self._cima = None
        self.tamano = 0

    def esta_vacia(self):
        return self._cima is None

    def apilar(self, dato):
        nodo = Nodo(dato)
        nodo.siguiente = self._cima
        self._cima = nodo
        self.tamano += 1

    def desapilar(self):                    #definicion de operaciones para la pila
        if self.esta_vacia():
            return None
        nodo = self._cima
        self._cima = nodo.siguiente 
        self.tamano -= 1
        return nodo.dato

    def ver_cima(self):
        if self.esta_vacia():
            return None
        return self._cima.dato


class Cola:
    def __init__(self):                          #clase de cola
        self._frente = None
        self._final = None
        self.tamano = 0

    def esta_vacia(self):
        return self._frente is None

    def encolar(self, dato):
        nodo = Nodo(dato)
        if self._final is None:
            self._frente = nodo
        else:                                              #definir operaciones para la cola
            self._final.siguiente = nodo
        self._final = nodo
        self.tamano += 1

    def desencolar(self):
        if self.esta_vacia():
            return None
        nodo = self._frente
        self._frente = nodo.siguiente
        if self._frente is None:
            self._final = None
        self.tamano -= 1
        return nodo.dato

class TablaHash:
    def __init__(self, capacidad=16):
        self.capacidad = capacidad                  #numero de cubetas donde se reparten las claves
        self.tamano = 0
        self._cubetas = [None] * capacidad          #cd cubeta guarda una cadena de nodos (clave, valor)

    def _indice(self, clave):
        return hash(clave) % self.capacidad         #FUNCION HASH: convierte la clave en la posicion de su cubeta

    def insertar(self, clave, valor):
        i = self._indice(clave)
        nodo = self._cubetas[i]
        while nodo is not None:
            if nodo.dato[0] == clave:
                nodo.dato = (clave, valor)          #la clave ya estaba, solo se reemplaza el valor
                return
            nodo = nodo.siguiente
        nuevo = Nodo((clave, valor))
        nuevo.siguiente = self._cubetas[i]          #colision: si la cubeta ya tenia algo, el nuevo se encadena al frente
        self._cubetas[i] = nuevo
        self.tamano += 1

    def obtener(self, clave):
        nodo = self._cubetas[self._indice(clave)]   #busqueda HASH: en vez de recorrer todo, solo recorre una cubeta, O(1) promedio
        while nodo is not None:
            if nodo.dato[0] == clave:
                return nodo.dato[1]
            nodo = nodo.siguiente
        return None

    def eliminar(self, clave):
        i = self._indice(clave)
        anterior = None
        nodo = self._cubetas[i]
        while nodo is not None:
            if nodo.dato[0] == clave:
                if anterior is None:
                    self._cubetas[i] = nodo.siguiente
                else:
                    anterior.siguiente = nodo.siguiente
                self.tamano -= 1
                return nodo.dato[1]
            anterior = nodo
            nodo = nodo.siguiente
        return None


def arreglo_ordenado_por_fecha(lista):
    ordenada = lista.copia()
    ordenada.ordenar_por(lambda x: x.due_date)      #se ordena primero porque la busqueda binaria solo sirve en datos ordenados
    return ordenada.a_arreglo()


def buscar_corte_por_fecha(arreglo, fecha):
    bajo = 0
    alto = len(arreglo)
    while bajo < alto:                              #busqueda binaria: devuelve la primera posicion con fecha mayor o igual a la buscada, O(log n)
        medio = (bajo + alto) // 2
        if arreglo[medio].due_date < fecha:
            bajo = medio + 1                        #la posicion buscada esta en la mitad derecha
        else:
            alto = medio                            #la posicion buscada esta en la mitad izquierda
    return bajo


def tramo(arreglo, inicio, fin):
    resultado = ListaEnlazada()
    for i in range(inicio, fin):                    #pasar a lista enlazada el pedazo que delimito la busqueda binaria
        resultado.agregar_al_final(arreglo[i])
    return resultado


STATUS_PENDING = "pending"                  
STATUS_DONE = "done"                                            #constantes para tarea, status y categorias
HOMEWORK_CATEGORIES = ["Tarea", "PIA", "Examen", "Otro"]

class Homework:
    def __init__(self, id, title, subject, category, due_date, status=STATUS_PENDING):
        self.id = id
        self.title = title
        self.subject = subject                            #clase de tarea y los parametros/variables que incluye
        self.category = category
        self.due_date = due_date
        self.status = status

    @property
    def is_overdue(self):                                                             #si el status de tarea es diferente a terminada y la fecha es menor a la de hoy, definirlo como vencida
        return self.status != STATUS_DONE and self.due_date < date.today()

    def is_due_soon(self, days=3):                  
        if self.status == STATUS_DONE:                 #si la tarea esta terminada, no marcar como pronto
            return False                          
        today = date.today()
        return today <= self.due_date <= today + timedelta(days=days)       


STATUS_UNPAID = "unpaid"
STATUS_PAID = "paid"                    #constantes para los recibos
BILL_CATEGORIES = [
    "Comida",
    "Transporte",
    "Material escolar",
    "Impresiones / copias",
    "Colegiatura / cuotas",
    "Tecnología",
    "Suscripciones",
    "Entretenimiento",
    "Salud",
    "Otro",
]

class Bill:
    def __init__(self, id, name, amount, category, due_date, status=STATUS_UNPAID):         #clase de recibo
        self.id = id
        self.name = name
        self.amount = amount
        self.category = category
        self.due_date = due_date
        self.status = status

    @property
    def is_overdue(self):
        return self.status != STATUS_PAID and self.due_date < date.today()

    def is_due_soon(self, days=3):
        if self.status == STATUS_PAID:
            return False
        today = date.today()
        return today <= self.due_date <= today + timedelta(days=days)


class Resumen:
    def __init__(self):
        self.tareas_atrasadas = ListaEnlazada()
        self.tareas_pronto = ListaEnlazada()
        self.tareas_pendientes = 0                                 #clase de resumen, definir las tareas y recibos como listas enlazadas
        self.recibos_atrasados = ListaEnlazada()
        self.recibos_pronto = ListaEnlazada()
        self.recibos_pendientes = 0


class Bitacora:
    def __init__(self):
        self._homeworks = ListaEnlazada()
        self._bills = ListaEnlazada()                               #clase de bitacora y definir las opciones como lista enlazada
        self._indice_tareas = TablaHash()                           #tablas hash que indexan por ID para no recorrer la lista completa
        self._indice_recibos = TablaHash()
        self._next_homework_id = 1
        self._next_bill_id = 1

    def add_homework(self, title, subject, category, due_date, status=STATUS_PENDING):
        homework = Homework(self._next_homework_id, title, subject, category, due_date, status)     #definicion para agregar tarea
        self._homeworks.agregar_al_final(homework)
        self._indice_tareas.insertar(homework.id, homework)                                 #se guarda tambien en la tabla hash
        self._next_homework_id += 1
        return homework

    def list_homeworks(self, status=None, category=None):
        seleccion = self._homeworks.copia()
        if status:
            seleccion = seleccion.filtrar(lambda h: h.status == status)                   #definir la lista de tareas, y filtraciones de status y categoria
        if category:
            seleccion = seleccion.filtrar(lambda h: h.category == category)
        seleccion.ordenar_por(lambda h: h.due_date)
        return seleccion

    def get_homework(self, homework_id):                                                #busqueda de tarea por ID resuelta con la tabla hash
        return self._indice_tareas.obtener(homework_id)

    def marcar_homework_hecha(self, homework_id):
        homework = self.get_homework(homework_id)                                        
        if homework is not None:
            homework.status = STATUS_DONE
        return homework

    def editar_homework(self, homework_id, title, subject, category, due_date):
        homework = self.get_homework(homework_id)
        if homework is not None:
            homework.title = title
            homework.subject = subject
            homework.category = category
            homework.due_date = due_date
        return homework

    def delete_homework(self, homework_id):
        if self._indice_tareas.eliminar(homework_id) is None:                               #la tabla hash dice si existe antes de recorrer la lista
            return False
        self._homeworks.eliminar(lambda h: h.id == homework_id)
        return True

    def add_bill(self, name, amount, category, due_date, status=STATUS_UNPAID):
        bill = Bill(self._next_bill_id, name, amount, category, due_date, status)
        self._bills.agregar_al_final(bill)
        self._indice_recibos.insertar(bill.id, bill)
        self._next_bill_id += 1
        return bill

    def list_bills(self, status=None, category=None):
        seleccion = self._bills.copia()
        if status:
            seleccion = seleccion.filtrar(lambda b: b.status == status)
        if category:
            seleccion = seleccion.filtrar(lambda b: b.category == category)
        seleccion.ordenar_por(lambda b: b.due_date)
        return seleccion

    def get_bill(self, bill_id):
        return self._indice_recibos.obtener(bill_id)                                        #misma busqueda por hash para los recibos

    def marcar_bill_pagado(self, bill_id):
        bill = self.get_bill(bill_id)
        if bill is not None:
            bill.status = STATUS_PAID
        return bill

    def editar_bill(self, bill_id, name, amount, category, due_date):
        bill = self.get_bill(bill_id)
        if bill is not None:
            bill.name = name
            bill.amount = amount
            bill.category = category
            bill.due_date = due_date
        return bill

    def delete_bill(self, bill_id):
        if self._indice_recibos.eliminar(bill_id) is None:
            return False
        self._bills.eliminar(lambda b: b.id == bill_id)
        return True

    def summary(self):
        datos = Resumen()
        hoy = date.today()
        corte_pronto = hoy + timedelta(days=4)                                      #limite exclusivo, asi cubre de hoy a maximo 3 dias

        tareas = self._homeworks.filtrar(lambda h: h.status == STATUS_PENDING)
        datos.tareas_pendientes = tareas.contar()
        arreglo = arreglo_ordenado_por_fecha(tareas)                                #1) ordenamiento por fecha
        inicio = buscar_corte_por_fecha(arreglo, hoy)                               #2) busqueda binaria del lugar donde empieza hoy
        datos.tareas_atrasadas = tramo(arreglo, 0, inicio)                          #lo que quedo antes de ese corte esta atrasado
        datos.tareas_pronto = tramo(arreglo, inicio, buscar_corte_por_fecha(arreglo, corte_pronto))

        recibos = self._bills.filtrar(lambda b: b.status == STATUS_UNPAID)
        datos.recibos_pendientes = recibos.contar()
        arreglo = arreglo_ordenado_por_fecha(recibos)
        inicio = buscar_corte_por_fecha(arreglo, hoy)
        datos.recibos_atrasados = tramo(arreglo, 0, inicio)
        datos.recibos_pronto = tramo(arreglo, inicio, buscar_corte_por_fecha(arreglo, corte_pronto))
        return datos


def read_nonempty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Este campo no puede quedar vacío.")


def parse_date(raw):
    return datetime.strptime(raw, "%Y-%m-%d").date()


def read_date(prompt):
    while True:
        raw = input(f"{prompt} (AAAA-MM-DD): ").strip()
        try:
            return parse_date(raw)
        except ValueError:
            print("Fecha inválida. Usa el formato AAAA-MM-DD, ej. 2026-09-15.")


def read_date_or_default(prompt, default):
    while True:
        raw = input(f"{prompt} [{default.isoformat()}] (AAAA-MM-DD): ").strip()
        if not raw:
            return default
        try:
            return parse_date(raw)
        except ValueError:
            print("Fecha inválida. Usa el formato AAAA-MM-DD, ej. 2026-09-15.")


def read_amount(prompt):
    while True:
        raw = input(prompt).strip()
        try:
            amount = Decimal(raw)
        except InvalidOperation:
            print("Cantidad inválida. Escribe un número, ej. 150.50")
            continue
        if amount < 0:
            print("La cantidad no puede ser negativa.")
            continue
        return amount


def read_amount_or_default(prompt, default):
    while True:
        raw = input(f"{prompt} [{default}]: ").strip()
        if not raw:
            return default
        try:
            amount = Decimal(raw)
        except InvalidOperation:
            print("Cantidad inválida. Escribe un número, ej. 150.50")
            continue
        if amount < 0:
            print("La cantidad no puede ser negativa.")
            continue
        return amount


def read_text_or_default(prompt, default):
    raw = input(f"{prompt} [{default or '-'}]: ").strip()
    return raw if raw else default


def choose_category(categories):
    print("Categorías disponibles:")
    for i, cat in enumerate(categories, start=1):
        print(f"  {i}. {cat}")
    print("  0. (sin categoría)")
    while True:
        raw = input("Elige una categoría: ").strip()
        if raw in ("0", ""):
            return None
        if raw.isdigit() and 1 <= int(raw) <= len(categories):
            return categories[int(raw) - 1]
        print("Opción inválida.")


def choose_category_or_default(categories, default):
    print(f"Categoría actual: {default or '(sin categoría)'}")
    for i, cat in enumerate(categories, start=1):
        print(f"  {i}. {cat}")
    print("  0. (sin categoría)")
    raw = input("Nueva categoría (Enter para mantener la actual): ").strip()
    if raw == "":
        return default
    if raw == "0":
        return None
    if raw.isdigit() and 1 <= int(raw) <= len(categories):
        return categories[int(raw) - 1]
    print("Opción inválida, se mantiene la categoría actual.")
    return default


def choose_id(lista, prompt):
    if lista.esta_vacia():
        return None
    while True:
        raw = input(prompt).strip()
        if raw.isdigit():
            elegido = int(raw)
            if lista.buscar(lambda x: x.id == elegido) is not None:
                return elegido
        print("ID inválido.")


def print_homeworks(homeworks):
    if homeworks.esta_vacia():
        print("No hay tareas para mostrar.")
        return
    print(f"{'ID':<4}{'Título':<25}{'Materia':<15}{'Categoría':<14}{'Vence':<12}{'Estado'}")
    for h in homeworks:
        estado = "Hecha" if h.status == STATUS_DONE else "Pendiente"
        if h.is_overdue:
            estado += " (VENCIDA)"
        elif h.is_due_soon():
            estado += " (por vencer)"
        print(
            f"{h.id:<4}{h.title:<25}{(h.subject or '-'):<15}"
            f"{(h.category or '-'):<14}{h.due_date.isoformat():<12}{estado}"
        )


def print_bills(bills):
    if bills.esta_vacia():
        print("No hay recibos para mostrar.")
        return
    print(f"{'ID':<4}{'Nombre':<25}{'Monto':<12}{'Categoría':<14}{'Vence':<12}{'Estado'}")
    for b in bills:
        estado = "Pagado" if b.status == STATUS_PAID else "Sin pagar"
        if b.is_overdue:
            estado += " (VENCIDO)"
        elif b.is_due_soon():
            estado += " (por vencer)"
        print(
            f"{b.id:<4}{b.name:<25}${b.amount:<11}{(b.category or '-'):<14}"
            f"{b.due_date.isoformat():<12}{estado}"
        )


def print_resumen(datos):
    print("\n===== Resumen =====")
    print(f"Tareas pendientes: {datos.tareas_pendientes}    "
        f"Recibos sin pagar: {datos.recibos_pendientes}")
    print("\n-- Atrasado --")
    _atender_avisos(datos.tareas_atrasadas, datos.recibos_atrasados)
    print("\n-- Vence pronto (próximos 3 días) --")
    _atender_avisos(datos.tareas_pronto, datos.recibos_pronto)


def _atender_avisos(tareas, recibos):
    juntos = ListaEnlazada()
    for t in tareas:
        juntos.agregar_al_final(t)
    for r in recibos:
        juntos.agregar_al_final(r)
    juntos.ordenar_por(lambda x: x.due_date)
    cola = Cola()
    for item in juntos:
        cola.encolar(item)
    if cola.esta_vacia():
        print("  (nada)")
        return
    while not cola.esta_vacia():
        print("  " + _linea_aviso(cola.desencolar()))


def _linea_aviso(item):
    fecha = item.due_date.isoformat()
    if isinstance(item, Homework):
        return f"[Tarea] {item.title} — vence {fecha}"
    return f"[Recibo] {item.name} (${item.amount}) — vence {fecha}"


def _pantalla_menu_principal():
    print("\n===== Menú principal =====")
    print("1. Tareas")
    print("2. Recibos")
    print("3. Resumen")
    print("4. Salir")
    return input("Elige una opción: ").strip()


def _pantalla_menu_tareas(bitacora):
    print("\n--- Tareas ---")
    print("1. Listar todas")
    print("2. Listar pendientes")
    print("3. Listar por categoría")        #definicion de menu de tareas
    print("4. Agregar tarea")
    print("5. Marcar como hecha")
    print("6. Editar tarea")
    print("7. Eliminar tarea")
    print("0. Volver al menú principal")
    opcion = input("Elige una opción: ").strip()

    if opcion == "1":
        print_homeworks(bitacora.list_homeworks())
    elif opcion == "2":
        print_homeworks(bitacora.list_homeworks(status=STATUS_PENDING))
    elif opcion == "3":
        categoria = choose_category(HOMEWORK_CATEGORIES)
        print_homeworks(bitacora.list_homeworks(category=categoria))            #if para opciones, si esta opcion, hace esto, sino esto
    elif opcion == "4":
        title = read_nonempty("Título: ")
        subject = read_nonempty("Materia: ")
        category = choose_category(HOMEWORK_CATEGORIES)
        due_date = read_date("Fecha límite")
        bitacora.add_homework(title, subject, category, due_date)
        print("Tarea agregada.")
    elif opcion == "5":
        pendientes = bitacora.list_homeworks(status=STATUS_PENDING)
        if pendientes.esta_vacia():
            print("No hay tareas pendientes.")
        else:
            print_homeworks(pendientes)
            hid = choose_id(pendientes, "ID de la tarea a marcar como hecha: ")
            bitacora.marcar_homework_hecha(hid)
            print("Tarea marcada como hecha.")
    elif opcion == "6":
        homeworks = bitacora.list_homeworks()
        if homeworks.esta_vacia():
            print("No hay tareas para editar.")
        else:
            print_homeworks(homeworks)
            hid = choose_id(homeworks, "ID de la tarea a editar: ")
            actual = bitacora.get_homework(hid)
            title = read_text_or_default("Título", actual.title)
            subject = read_text_or_default("Materia", actual.subject)
            category = choose_category_or_default(HOMEWORK_CATEGORIES, actual.category)
            due_date = read_date_or_default("Fecha límite", actual.due_date)
            bitacora.editar_homework(hid, title, subject, category, due_date)
            print("Tarea actualizada.")
    elif opcion == "7":
        homeworks = bitacora.list_homeworks()
        if homeworks.esta_vacia():
            print("No hay tareas para eliminar.")
        else:
            print_homeworks(homeworks)
            hid = choose_id(homeworks, "ID de la tarea a eliminar: ")
            bitacora.delete_homework(hid)
            print("Tarea eliminada.")
    elif opcion == "0":
        return False
    else:
        print("Opción inválida.")
    return True

def _pantalla_menu_recibos(bitacora):
    print("\n--- Recibos ---")
    print("1. Listar todos")
    print("2. Listar sin pagar")
    print("3. Listar por categoría")                                #definición de menu recibos
    print("4. Agregar recibo")
    print("5. Marcar como pagado")
    print("6. Editar recibo")
    print("7. Eliminar recibo")
    print("0. Volver al menú principal")
    opcion = input("Elige una opción: ").strip()

    if opcion == "1":
        print_bills(bitacora.list_bills())
    elif opcion == "2":
        print_bills(bitacora.list_bills(status=STATUS_UNPAID))
    elif opcion == "3":
        categoria = choose_category(BILL_CATEGORIES)
        print_bills(bitacora.list_bills(category=categoria))            
    elif opcion == "4":
        name = read_nonempty("Nombre del recibo: ")
        amount = read_amount("Monto: ")
        category = choose_category(BILL_CATEGORIES)
        due_date = read_date("Fecha límite de pago")
        bitacora.add_bill(name, amount, category, due_date)
        print("Recibo agregado.")
    elif opcion == "5":
        sin_pagar = bitacora.list_bills(status=STATUS_UNPAID)
        if sin_pagar.esta_vacia():
            print("No hay recibos sin pagar.")
        else:
            print_bills(sin_pagar)
            bid = choose_id(sin_pagar, "ID del recibo a marcar como pagado: ")
            bitacora.marcar_bill_pagado(bid)
            print("Recibo marcado como pagado.")
    elif opcion == "6":
        bills = bitacora.list_bills()
        if bills.esta_vacia():
            print("No hay recibos para editar.")
        else:
            print_bills(bills)
            bid = choose_id(bills, "ID del recibo a editar: ")
            actual = bitacora.get_bill(bid)
            name = read_text_or_default("Nombre", actual.name)
            amount = read_amount_or_default("Monto", actual.amount)
            category = choose_category_or_default(BILL_CATEGORIES, actual.category)
            due_date = read_date_or_default("Fecha límite", actual.due_date)
            bitacora.editar_bill(bid, name, amount, category, due_date)
            print("Recibo actualizado.")
    elif opcion == "7":
        bills = bitacora.list_bills()
        if bills.esta_vacia():
            print("No hay recibos para eliminar.")
        else:
            print_bills(bills)
            bid = choose_id(bills, "ID del recibo a eliminar: ")
            bitacora.delete_bill(bid)
            print("Recibo eliminado.")
    elif opcion == "0":
        return False
    else:
        print("Opción inválida.")
    return True


def main():
    bitacora = Bitacora()
    print("Bitácora")

    pantallas = Pila()
    pantallas.apilar("principal")

    while not pantallas.esta_vacia():
        actual = pantallas.ver_cima()

        if actual == "principal":
            opcion = _pantalla_menu_principal()
            if opcion == "1":
                pantallas.apilar("tareas")              #aqui se ocupan pilas, en caso 1 muestra las tareas, 2 recibos, 3 resumen y 4 termina, cualquier otro es invalido
            elif opcion == "2":
                pantallas.apilar("recibos")
            elif opcion == "3":
                print_resumen(bitacora.summary())       
            elif opcion == "4":
                pantallas.desapilar()
            else:
                print("Opción inválida.")
        elif actual == "tareas":
            if not _pantalla_menu_tareas(bitacora):
                pantallas.desapilar()
        elif actual == "recibos":
            if not _pantalla_menu_recibos(bitacora):
                pantallas.desapilar()

    print("byebye.")

if __name__ == "__main__":
    main()
