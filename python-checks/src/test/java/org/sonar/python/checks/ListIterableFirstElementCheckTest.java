/*
 * SonarQube Python Plugin
 * Copyright (C) SonarSource Sàrl
 * mailto:info AT sonarsource DOT com
 *
 * You can redistribute and/or modify this program under the terms of
 * the Sonar Source-Available License Version 1, as published by SonarSource Sàrl.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * See the Sonar Source-Available License for more details.
 *
 * You should have received a copy of the Sonar Source-Available License
 * along with this program; if not, see https://sonarsource.com/license/ssal/
 */
package org.sonar.python.checks;

import java.util.stream.Stream;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;
import org.sonar.python.checks.quickfix.PythonQuickFixVerifier;
import org.sonar.python.checks.utils.PythonCheckVerifier;

class ListIterableFirstElementCheckTest {

  private static final ListIterableFirstElementCheck check = new ListIterableFirstElementCheck();

  @Test
  void test() {
    PythonCheckVerifier.verify("src/test/resources/checks/listIterableFirstElement.py", check);
  }

  static Stream<Arguments> quickFixTestCases() {
    return Stream.of(
      Arguments.of("list(get_users())[0]", "next(iter(get_users()))"),
      Arguments.of("list(users)[0]", "next(iter(users))"),
      Arguments.of("list(x for x in range(10))[0]", "next(iter(x for x in range(10)))"),
      Arguments.of("list(filter(None, items))[0]", "next(iter(filter(None, items)))")
    );
  }

  @ParameterizedTest
  @MethodSource("quickFixTestCases")
  void test_quick_fix(String codeWithIssue, String correctCode) {
    PythonQuickFixVerifier.verify(check, codeWithIssue, correctCode);
  }

  @Test
  void test_quick_fix_message() {
    String codeWithIssue = "list(get_users())[0]";

    PythonQuickFixVerifier.verifyQuickFixMessages(check, codeWithIssue, "Replace with \"next(iter(...))\"");
  }

  @Test
  void test_no_quick_fix_multiline_argument_expression() {
    String codeWithIssue = """
      list(
          get_items(
              arg
          )
      )[0]
      """;

    PythonQuickFixVerifier.verifyNoQuickFixes(check, codeWithIssue);
  }
}
