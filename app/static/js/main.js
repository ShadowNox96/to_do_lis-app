const bdelete = document.querySelectorAll('.btn-delete')

if(bdelete){
    const barray = Array.from(bdelete);
    
    barray.forEach((btn) => {
        btn.addEventListener('click', (e) =>{
            if(!confirm('Seguro que desea eliminar esta tarea?')){
                e.preventDefault();
            }
        });
        });
}