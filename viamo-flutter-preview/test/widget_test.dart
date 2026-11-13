import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:viamo_social/main.dart';

void main() {
  testWidgets('Viamo social feed starts in Bologna', (tester) async {
    tester.view.physicalSize = const Size(390, 850);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    await tester.pumpWidget(const Viamo());
    expect(find.text('viamo'), findsOneWidget);
    expect(find.textContaining('Italia, slik folk opplever det.'), findsOneWidget);
    expect(find.text('Strøm'), findsOneWidget);
  });
}
