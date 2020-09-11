package triangle;

import org.junit.Test;
import static org.junit.Assert.*;

import static triangle.Triangle.Type;
import static triangle.Triangle.Type.*;

/**
 * Test class for the Triangle implementation.
 */
public class TriangleTest {

    @Test
    public void test1() {
        Type actual = Triangle.classify(-1, 0, 1);
        Type expected = INVALID;
        assertEquals(expected, actual);
    }
	
    @Test
    public void test2() {
        Type actual = Triangle.classify(0, 0, 0);
        Type expected = INVALID;
        assertEquals(expected, actual);
    }
}
