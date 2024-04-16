function confirmSubmit()
{
    var agree=confirm("Czy na pewno chcesz usunąć zdjęcie? Tego procesu nie da się cofnąć!");
    if (agree)
        return true ;
    else
        return false ;
}