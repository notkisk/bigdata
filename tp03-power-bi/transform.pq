let
    Source = Csv.Document(File.Contents("File.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Types = Table.TransformColumnTypes(Headers, {{"Date", type date}, {"Region", type text}, {"Category", type text}, {"Sales", type number}, {"Quantity", Int64.Type}}),
    CleanText = Table.TransformColumns(Types, {{"Region", Text.Trim, type text}, {"Category", Text.Trim, type text}}),
    Filled = Table.ReplaceValue(CleanText, null, 0, Replacer.ReplaceValue, {"Sales", "Quantity"}),
    Unique = Table.Distinct(Filled)
in
    Unique
