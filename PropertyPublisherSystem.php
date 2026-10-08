<?php

namespace RealEstatePlatform;

interface ExportableInterface {
    public function toArray(): array;
    public function toHtmlCard(): string;
}

class ConstructionDetail {
    public string $developerName;
    public string $architecturalStyle;
    public int $yearBuilt;
    public string $constructionStatus;

    public function __construct(string $developerName, string $architecturalStyle, int $yearBuilt, string $constructionStatus) {
        $this->developerName = $developerName;
        $this->architecturalStyle = $architecturalStyle;
        $this->yearBuilt = $yearBuilt;
        $this->constructionStatus = $constructionStatus;
    }
}

class ListingItem implements ExportableInterface {
    private string $id;
    private string $title;
    private float $price;
    private string $location;
    private ConstructionDetail $details;
    private array $mediaGallery = [];

    public function __construct(string $title, float $price, string $location, ConstructionDetail $details) {
        $this->id = "LISTING-" . uniqid();
        $this->title = $title;
        $this->price = $price;
        $this->location = $location;
        $this->details = $details;
    }

    public function addMediaUrl(string $url): void {
        $this->mediaGallery[] = $url;
    }

    public function getPriceFormatted(): string {
        return "$" . number_format($this->price, 2);
    }

    public function toArray(): array {
        return [
            'id' => $this->id,
            'title' => $this->title,
            'price' => $this->price,
            'formatted_price' => $this->getPriceFormatted(),
            'location' => $this->location,
            'developer' => $this->details->developerName,
            'status' => $this->details->constructionStatus,
            'media_count' => count($this->mediaGallery)
        ];
    }

    public function toHtmlCard(): string {
        $heroImage = $this->mediaGallery[0] ?? 'https://via.placeholder.com/600x400';
        return "
        <div class='property-card' id='{$this->id}'>
            <img src='{$heroImage}' alt='{$this->title}' class='property-thumb' />
            <div class='property-info'>
                <h2>{$this->title}</h2>
                <p class='price'>{$this->getPriceFormatted()}</p>
                <p class='location'>📍 {$this->location}</p>
                <p class='status'>Status: <strong>{$this->details->constructionStatus}</strong></p>
                <p class='style'>Style: {$this->details->architecturalStyle}</p>
            </div>
        </div>
        ";
    }
}

class ListingRepository {
    private array $listings = [];

    public function addListing(ListingItem $listing): void {
        $this->listings[] = $listing;
    }

    public function renderAllCards(): string {
        $output = "<div class='property-grid'>\n";
        foreach ($this->listings as $listing) {
            $output .= $listing->toHtmlCard();
        }
        $output .= "</div>";
        return $output;
    }
}

// Execution Script
$detail = new ConstructionDetail("BuildCorp Global", "Modern Minimalist", 2026, "Under Construction");
$listing = new ListingItem("Urban Heights Residence", 850000.00, "Downtown Central", $detail);

$listing->addMediaUrl("https://images.site/render1.jpg");
$listing->addMediaUrl("https://images.site/render2.jpg");

$repo = new ListingRepository();
$repo->addListing($listing);

header('Content-Type: text/html; charset=utf-8');
echo $repo->renderAllCards();