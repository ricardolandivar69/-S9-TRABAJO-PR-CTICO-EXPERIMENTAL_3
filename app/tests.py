from django.test import TestCase
from .models import Tarea


class TareaModelTest(TestCase):

    def test_crear_tarea(self):
        tarea = Tarea.objects.create(
            titulo="Configurar integración continua",
            descripcion="Prueba automatizada del modelo Tarea"
        )

        self.assertEqual(
            tarea.titulo,
            "Configurar integración continua"
        )

        self.assertFalse(tarea.completada)