import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:url_launcher/url_launcher.dart';

void main() {
  runApp(const StackQnaApp());
}

class StackQnaApp extends StatelessWidget {
  const StackQnaApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Stack Overflow RAG Q&A',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const QnAScreen(),
    );
  }
}

class QnAScreen extends StatefulWidget {
  const QnAScreen({super.key});

  @override
  State<QnAScreen> createState() => _QnAScreenState();
}

class _QnAScreenState extends State<QnAScreen> {
  final TextEditingController _controller = TextEditingController();
  final TextEditingController _tagsController = TextEditingController();
  final ScrollController _scrollController = ScrollController(); // Add this
  String _selectedSource = 'hf';
  bool _loading = false;
  String? _error;
  Map<String, dynamic>? _result;
  int? _selectedSourceIndex; // Track selected row

  String? _llmAnswer;
  String? _llmSourceUrl;
  bool _llmLoading = false;
  double _minScore = 0;

  Future<void> _askQuestion() async {
    setState(() {
      _loading = true;
      _error = null;
      _result = null;
      _selectedSourceIndex = null;
    });
    try {
      List<String>? tags;
      if (_tagsController.text.trim().isNotEmpty) {
        tags = _tagsController.text
            .split(',')
            .map((t) => t.trim())
            .where((t) => t.isNotEmpty)
            .toList();
      }
      final response = await http.post(
        Uri.parse('http://127.0.0.1:8001/ask'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'question': _controller.text,
          'source': _selectedSource,
          if (tags != null && tags.isNotEmpty) 'tags': tags,
          if (_minScore > 0) 'min_score': _minScore.toInt(),
        }),
      );
      if (response.statusCode == 200) {
        setState(() {
          _result = jsonDecode(response.body);
        });
      } else {
        setState(() {
          _error = 'Error: ${response.statusCode} ${response.reasonPhrase}';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Error: $e';
      });
    } finally {
      setState(() {
        _loading = false;
      });
    }
  }

  Future<void> _generateLlmAnswer() async {
    setState(() {
      _llmLoading = true;
      _error = null;
      _llmAnswer = null;
      _llmSourceUrl = null;
    });
    try {
      final response = await http.post(
        Uri.parse('http://127.0.0.1:8001/ask_llm'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'question': _controller.text}),
      );
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        setState(() {
          _llmAnswer = data['answer'] ?? '';
          _llmSourceUrl = data['source_url'] ?? '';
        });
      } else {
        setState(() {
          _error =
              'LLM Error: \\${response.statusCode} \\${response.reasonPhrase}';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'LLM Error: $e';
      });
    } finally {
      setState(() {
        _llmLoading = false;
      });
    }
  }

  Widget _buildSourceChip(Map<String, dynamic> src) {
    final tags = (src['tags'] as List?)?.join(', ') ?? '';
    final score = src['score'] ?? 0;
    final favs = src['favorite_count'] ?? 0;
    final accepted = src['accepted_answer_id'] != null;
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 8),
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (accepted)
              Row(
                children: [
                  Icon(Icons.check_circle, color: Colors.green, size: 20),
                  const SizedBox(width: 6),
                  Text(
                    'Accepted Answer',
                    style: TextStyle(color: Colors.green),
                  ),
                ],
              ),
            SelectableText(
              src['question'] ?? '',
              style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
            ),
            const SizedBox(height: 8),
            SelectableText(src['answer'] ?? ''),
            const SizedBox(height: 8),
            Wrap(
              spacing: 8,
              children: [
                if (tags.isNotEmpty) Chip(label: Text('Tags: $tags')),
                Chip(label: Text('Score: $score')),
                Chip(label: Text('Favorites: $favs')),
              ],
            ),
          ],
        ),
      ),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    _tagsController.dispose();
    _scrollController.dispose(); // Dispose the controller
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Stack Overflow RAG Q&A'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            tooltip: 'Refresh',
            onPressed: () {
              setState(() {
                _controller.clear();
                _tagsController.clear();
                _selectedSource = 'hf';
                _loading = false;
                _error = null;
                _result = null;
                _selectedSourceIndex = null;
                _llmAnswer = null;
                _llmSourceUrl = null;
                _llmLoading = false;
                _minScore = 0;
              });
            },
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Scrollbar(
          controller: _scrollController,
          thumbVisibility: true,
          child: SingleChildScrollView(
            controller: _scrollController,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                TextField(
                  controller: _controller,
                  decoration: const InputDecoration(
                    labelText: 'Ask a programming question',
                    border: OutlineInputBorder(),
                  ),
                  onSubmitted: (_) => _askQuestion(),
                ),
                const SizedBox(height: 12),
                Row(
                  children: [
                    const Text('Data Source:'),
                    const SizedBox(width: 12),
                    DropdownButton<String>(
                      value: _selectedSource,
                      items: const [
                        DropdownMenuItem(value: 'local', child: Text('Local')),
                        DropdownMenuItem(
                          value: 'hf',
                          child: Text('Hugging Face'),
                        ),
                        DropdownMenuItem(
                          value: 'llm',
                          child: Text('LLM (future)'),
                        ),
                      ],
                      onChanged: (v) =>
                          setState(() => _selectedSource = v ?? 'hf'),
                    ),
                    const Spacer(),
                    ElevatedButton(
                      onPressed: _loading ? null : _askQuestion,
                      child: _loading
                          ? const SizedBox(
                              width: 18,
                              height: 18,
                              child: CircularProgressIndicator(strokeWidth: 2),
                            )
                          : const Text('Ask'),
                    ),
                  ],
                ),
                const SizedBox(height: 12),
                Row(
                  children: [
                    Expanded(
                      child: TextField(
                        controller: _tagsController,
                        decoration: const InputDecoration(
                          labelText: 'Tags (comma separated)',
                          border: OutlineInputBorder(),
                        ),
                      ),
                    ),
                    const SizedBox(width: 12),
                    SizedBox(
                      width: 120,
                      child: Row(
                        children: [
                          const Text('Min Score:'),
                          Expanded(
                            child: Slider(
                              value: _minScore,
                              min: 0,
                              max: 100,
                              divisions: 20,
                              label: _minScore.round().toString(),
                              onChanged: (v) => setState(() => _minScore = v),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 18),
                if (_error != null)
                  SelectableText(
                    _error!,
                    style: const TextStyle(color: Colors.red),
                  ),
                if (_result != null) ...[
                  Text(
                    'Answer:',
                    style: Theme.of(context).textTheme.titleMedium,
                  ),
                  const SizedBox(height: 8),
                  SelectableText(
                    _result!["answer"] ?? '',
                    style: const TextStyle(fontSize: 16),
                  ),
                  const SizedBox(height: 16),
                  ElevatedButton.icon(
                    onPressed: _llmLoading ? null : _generateLlmAnswer,
                    icon: const Icon(Icons.auto_awesome),
                    label: _llmLoading
                        ? const SizedBox(
                            width: 18,
                            height: 18,
                            child: CircularProgressIndicator(strokeWidth: 2),
                          )
                        : const Text('Generate LLM Answer'),
                  ),
                  if (_llmAnswer != null) ...[
                    const SizedBox(height: 16),
                    Text(
                      'LLM Answer:',
                      style: Theme.of(context).textTheme.titleMedium,
                    ),
                    const SizedBox(height: 8),
                    SelectableText(
                      _llmAnswer ?? '',
                      style: const TextStyle(fontSize: 16),
                    ),
                    if (_llmSourceUrl != null && _llmSourceUrl!.isNotEmpty)
                      Padding(
                        padding: const EdgeInsets.only(top: 4.0),
                        child: InkWell(
                          onTap: () => launchUrl(Uri.parse(_llmSourceUrl!)),
                          child: Text(
                            _llmSourceUrl!,
                            style: const TextStyle(
                              color: Colors.blue,
                              decoration: TextDecoration.underline,
                            ),
                          ),
                        ),
                      ),
                  ],
                  const SizedBox(height: 16),
                  if ((_result!["sources"] as List).isNotEmpty)
                    Text(
                      'Sources:',
                      style: Theme.of(context).textTheme.titleMedium,
                    ),
                  if ((_result!["sources"] as List).isNotEmpty)
                    SingleChildScrollView(
                      scrollDirection: Axis.horizontal,
                      child: DataTable(
                        columns: const [
                          DataColumn(label: Text('Accepted')),
                          DataColumn(label: Text('Question')),
                          DataColumn(label: Text('Answer')),
                          DataColumn(label: Text('Tags')),
                          DataColumn(label: Text('Score')),
                          DataColumn(label: Text('Favorites')),
                        ],
                        rows: (_result!["sources"] as List).asMap().entries.map(
                          (entry) {
                            final idx = entry.key;
                            final s = entry.value as Map<String, dynamic>;
                            final tags = (s['tags'] as List?)?.join(', ') ?? '';
                            final accepted = s['accepted_answer_id'] != null;
                            return DataRow(
                              selected: _selectedSourceIndex == idx,
                              onSelectChanged: (selected) {
                                setState(() {
                                  _selectedSourceIndex = selected! ? idx : null;
                                });
                              },
                              cells: [
                                DataCell(
                                  accepted
                                      ? const Icon(
                                          Icons.check_circle,
                                          color: Colors.green,
                                          size: 18,
                                        )
                                      : const SizedBox.shrink(),
                                ),
                                DataCell(SelectableText(s['question'] ?? '')),
                                DataCell(SelectableText(s['answer'] ?? '')),
                                DataCell(Text(tags)),
                                DataCell(Text('${s['score'] ?? 0}')),
                                DataCell(Text('${s['favorite_count'] ?? 0}')),
                              ],
                            );
                          },
                        ).toList(),
                      ),
                    ),
                  if (_selectedSourceIndex != null)
                    Padding(
                      padding: const EdgeInsets.only(top: 16.0),
                      child: Card(
                        elevation: 2,
                        child: Padding(
                          padding: const EdgeInsets.all(16.0),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                'Selected Source',
                                style: Theme.of(context).textTheme.titleMedium,
                              ),
                              const SizedBox(height: 8),
                              Text(
                                'Question:',
                                style: const TextStyle(
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              const SizedBox(height: 4),
                              SelectableText(
                                ((_result!["sources"]
                                            as List)[_selectedSourceIndex!]
                                        as Map<String, dynamic>)['question'] ??
                                    '',
                              ),
                              const SizedBox(height: 8),
                              Text(
                                'Answer:',
                                style: const TextStyle(
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              const SizedBox(height: 4),
                              SelectableText(
                                ((_result!["sources"]
                                            as List)[_selectedSourceIndex!]
                                        as Map<String, dynamic>)['answer'] ??
                                    '',
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                  const SizedBox(height: 8),
                  SelectableText(
                    'Tokens: \u001b[36m[0m${_result!["tokens"] ?? 0}',
                  ),
                  SelectableText('Status: ${_result!["status"] ?? ""}'),
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }
}
