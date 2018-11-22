import junit.framework.*;
public class MaClasseTest extends TestCase{
    public void testCalculer() throws Exception {
        assertEquals(2,MaClass.calculer(1,1));
    }
    public void testCalculer2() throws Exception {
        assertEquals("Sur l'entree (1,1), votre fonction n'a pas fait ce qui était attendu",2,MaClass.calculer(1,1));
    }
    public void testCalculer3() throws Exception {

        assertEquals("Sur l'entree (1,2), votre fonction n'a pas fait ce qui était attendu",3,MaClass.calculer(1,2));
    }
    public void testCalculer4() throws Exception {
        assertEquals("Sur l'entree (3,1), votre fonction n'a pas fait ce qui était attendu",4,MaClass.calculer(3,1));
    }
}
