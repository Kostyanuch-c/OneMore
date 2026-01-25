interface SetProblem {
  id: string;
  number: number;
  question: string;
  difficulty: "легкая" | "средняя" | "сложная";
  answer: string;
  hint?: string;
}

export interface ProblemSet {
  id: string;
  title: string;
  description: string;
  problems: SetProblem[];
}

export const problemSetsData: ProblemSet[] = [
  {
    id: "set-1",
    title: "Общая химия I",
    description:
      "Основные задачи по стехиометрии, атомному строению и химическим реакциям",
    problems: [
      {
        id: "p1",
        number: 1,
        question:
          "Сколько молей O₂ необходимо для реакции с 2 молями CH₄ при полном сгорании?",
        difficulty: "легкая",
        answer: "4 моля O₂ (CH₄ + 2O₂ → CO₂ + 2H₂O)",
        hint: "Сначала запишите уравненную реакцию",
      },
      {
        id: "p2",
        number: 2,
        question: "Вычислите молярную массу Ca(OH)₂",
        difficulty: "легкая",
        answer: "74,09 г/моль (Ca: 40,08 + O: 2×16,00 + H: 2×1,01)",
      },
      {
        id: "p3",
        number: 3,
        question: "Какова электронная конфигурация Fe²⁺?",
        difficulty: "средняя",
        answer: "[Ar] 3d⁶ (теряет 2 электрона с 4s орбитали)",
        hint: "Железо теряет электроны с 4s до 3d",
      },
      {
        id: "p4",
        number: 4,
        question: "Вычислите pH раствора 0,01 М HCl",
        difficulty: "легкая",
        answer: "pH = 2 (pH = -log[H⁺] = -log(0,01))",
      },
      {
        id: "p5",
        number: 5,
        question:
          "Сколько граммов NaCl необходимо для приготовления 500 мл раствора 0,5 М?",
        difficulty: "средняя",
        answer: "14,61 г (моли = 0,5 × 0,5 = 0,25 моль, масса = 0,25 × 58,44)",
        hint: "Используйте M = моль/л и молярную массу NaCl",
      },
    ],
  },
  {
    id: "set-2",
    title: "Органическая химия",
    description:
      "Задачи по номенклатуре, реакциям и механизмам в органической химии",
    problems: [
      {
        id: "p1",
        number: 1,
        question: "Назовите соединение: CH₃CH₂CH₂CH₃",
        difficulty: "легкая",
        answer: "Бутан",
      },
      {
        id: "p2",
        number: 2,
        question: "Каков продукт присоединения HBr к пропену?",
        difficulty: "средняя",
        answer: "2-бромпропан (по правилу Марковникова)",
        hint: "Правило Марковникова: H присоединяется к углероду с большим числом атомов H",
      },
      {
        id: "p3",
        number: 3,
        question: "Определите функциональную группу в CH₃COOH",
        difficulty: "легкая",
        answer: "Карбоксильная кислота (-COOH)",
      },
      {
        id: "p4",
        number: 4,
        question: "Нарисуйте все конституционные изомеры C₄H₁₀",
        difficulty: "сложная",
        answer: "Два изомера: н-бутан и 2-метилпропан (изобутан)",
      },
    ],
  },
  {
    id: "set-3",
    title: "Термодинамика",
    description: "Расчеты энергии, энтальпии, энтропии и свободной энергии",
    problems: [
      {
        id: "p1",
        number: 1,
        question:
          "Вычислите ΔH реакции, если ΔH(продукты) = -200 кДж и ΔH(реагенты) = -50 кДж",
        difficulty: "легкая",
        answer: "-150 кДж (ΔH = ΔH(продукты) - ΔH(реагенты))",
      },
      {
        id: "p2",
        number: 2,
        question: "Спонтанна ли реакция, если ΔG = -25 кДж/моль?",
        difficulty: "легкая",
        answer: "Да, отрицательное ΔG указывает на спонтанную реакцию",
      },
      {
        id: "p3",
        number: 3,
        question: "Вычислите ΔS для процесса, где q = 500 Дж и T = 298 К",
        difficulty: "средняя",
        answer: "1,68 Дж/К (ΔS = q/T = 500/298)",
        hint: "Используйте ΔS = q/T для обратимых процессов",
      },
    ],
  },
];
