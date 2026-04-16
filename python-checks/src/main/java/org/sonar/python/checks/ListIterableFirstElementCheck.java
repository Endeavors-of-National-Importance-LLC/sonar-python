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

import org.sonar.check.Rule;
import org.sonar.plugins.python.api.PythonSubscriptionCheck;
import org.sonar.plugins.python.api.SubscriptionContext;
import org.sonar.plugins.python.api.quickfix.PythonQuickFix;
import org.sonar.plugins.python.api.tree.CallExpression;
import org.sonar.plugins.python.api.tree.NumericLiteral;
import org.sonar.plugins.python.api.tree.RegularArgument;
import org.sonar.plugins.python.api.tree.SubscriptionExpression;
import org.sonar.plugins.python.api.tree.Tree;
import org.sonar.plugins.python.api.types.v2.matchers.TypeMatcher;
import org.sonar.plugins.python.api.types.v2.matchers.TypeMatchers;
import org.sonar.python.quickfix.TextEditUtils;
import org.sonar.python.tree.NumericLiteralImpl;
import org.sonar.python.tree.TreeUtils;

@Rule(key = "S8519")
public class ListIterableFirstElementCheck extends PythonSubscriptionCheck {

  private static final String MESSAGE = "Replace \"list(...)[0]\" with \"next(iter(...))\" to avoid materializing the entire iterable.";
  private static final TypeMatcher IS_LIST = TypeMatchers.isType("list");

  @Override
  public void initialize(Context context) {
    context.registerSyntaxNodeConsumer(Tree.Kind.SUBSCRIPTION, ListIterableFirstElementCheck::checkSubscription);
  }

  private static void checkSubscription(SubscriptionContext ctx) {
    SubscriptionExpression subscriptionExpression = (SubscriptionExpression) ctx.syntaxNode();

    var subscripts = subscriptionExpression.subscripts();
    if (!subscripts.commas().isEmpty() || subscripts.expressions().size() != 1) {
      return;
    }

    var subscript = subscripts.expressions().get(0);
    if (!(subscript instanceof NumericLiteral numericLiteral)) {
      return;
    }
    if (!isIntegerLiteralSubscript(numericLiteral)) {
      return;
    }
    long indexValue;
    try {
      indexValue = numericLiteral.valueAsLong();
    } catch (NumberFormatException e) {
      return;
    }
    if (indexValue != 0L) {
      return;
    }

    if (!(subscriptionExpression.object() instanceof CallExpression listCall)) {
      return;
    }

    if (!IS_LIST.isTrueFor(listCall.callee(), ctx)) {
      return;
    }

    if (listCall.arguments().size() != 1 || !(listCall.arguments().get(0) instanceof RegularArgument regularArg)) {
      return;
    }

    PreciseIssue issue = ctx.addIssue(listCall.callee(), MESSAGE);

    String argText = TreeUtils.treeToString(regularArg.expression(), false);
    if (argText != null && !argText.contains("\n")) {
      PythonQuickFix quickFix = PythonQuickFix.newQuickFix("Replace with \"next(iter(...))\"",
        TextEditUtils.replace(subscriptionExpression, "next(iter(" + argText + "))"));
      issue.addQuickFix(quickFix);
    }
  }

  private static boolean isIntegerLiteralSubscript(NumericLiteral literal) {
    if (literal instanceof NumericLiteralImpl impl) {
      return impl.numericKind() == NumericLiteralImpl.NumericKind.INT;
    }
    return false;
  }
}
