from app.models.CCO import CCO
from app.utils.to_txt import TO_TXT
from app.utils.to_vtk import TO_VTK

cco = CCO("/home/pedro/Downloads/UFOP/Periodo8/Monografia1/Codes/xml_to_vtk_n_txt/docs/tree_2D.xml")
to_txt = TO_TXT(cco)
to_vtk = TO_VTK(cco)