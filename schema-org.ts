/**
 * Schema.org TypeScript Definitions
 * Comprehensive schema covering all major Schema.org types
 * https://schema.org/docs/schemas.html
 */

// =============================================================================
// CORE TYPES - Foundation types that other types extend
// =============================================================================

/** The most generic type of item. */
interface Thing {
  /** URL of the item */
  id?: string;
  /** Name of the item */
  name?: string;
  /** A natural language name for the item */
  alternateName?: string;
  /** A short description of the item */
  description?: string;
  /** A sub property of description. A textual description of the item from another source */
  disambiguatingDescription?: string;
  /** URL of an image of the item */
  image?: string | ImageObject;
  /** URL of a reference page that unambiguously indicates the item's identity */
  url?: string;
}

/** The minimum viable amount of a credit. */
interface PronounceableText {
  text?: string;
  phoneticText?: string;
}

// =============================================================================
// Creative Works - Audio, Visual, Written, or otherwise creative content
// =============================================================================

/** A creative work, including books, movies, photographs, software, etc. */
interface CreativeWork extends Thing {
  /** The subject matter of the content */
  about?: Thing;
  /** Indicates that the CreativeWork contains a reference to a Target. */
  abstract?: string;
  /** The human sensory perceptual (or cognitive) property */
  accessMode?: string;
  /** The mode of the audio/information (text, visual, etc.) */
  accessModeSufficient?: AccessModeSpecification;
  /** Specifies the number of accesses to the item */
  accessibilityAPI?: string;
  /** Text indicating content type. Text, Image, audio, video */
  accessibilityFeature?: string;
  /** A characteristic of the described resource */
  accessibilityHazard?: string;
  /** A collection of data */
  associatedMedia?: MediaObject;
  /** The intended audience */
  audience?: Audience;
  /** The media objects that encode the creative work */
  encoding?: MediaObject;
  /** Event id/URL */
  event?: Event;
  /** Text of a user review */
  hasPart?: CreativeWork;
  /** A musical recording */
  isAccessibleForFree?: boolean;
  /** Position relative to other items */
  position?: number;
  /** Version of the creative work */
  version?: number | string;
  /** Fictional person */
  character?: Person;
  /** Organization or person who provides a copy */
  provider?: Organization | Person;
  /** Publisher's embedded social info */
  publishedBy?: Organization | Person;
  /** Rights management info */
  copyrightNotice?: string;
  /** Link to official resource */
  mainEntity?: Thing;
  /** Schema.org URL or id */
  schemaVersion?: string;
  /** Alternative head */
  alternativeHeadline?: string;
  /** Time required to watch */
  timeRequired?: string;
  /** Related links/URLs */
  relatedLink?: string;
  /** Corrected version */
  workExample?: CreativeWork;
}

/** A book */
interface Book extends CreativeWork {
  bookEdition?: string;
  bookFormat?: BookFormatType;
  illustrator?: Person;
  author?: Person;
  numberOfPages?: number;
}

/** Book format enumeration */
type BookFormatType = 
  | "http://schema.org/AudiobookFormat"
  | "http://schema.org/EBook"
  | "http://schema.org/Hardcover"
  | "http://schema.org/Paperback";

/** A written text meant for a human reading */
interface Article extends CreativeWork {
  articleSection?: string;
  articleBody?: string;
  pageEnd?: number;
  pageStart?: number;
  pagination?: string;
  wordCount?: number;
  /** The person or organization */
  publishedBy?: Organization | Person;
  /** Approvals */
  approved?: boolean;
  /** Associated images */
  image?: string | ImageObject;
}

/** Content in a format like blog posts */
interface BlogPosting extends Article {
  headline?: string;
  audio?: MusicGroup;
  video?: VideoObject;
}

/** A specific segment of content */
interface BlogPost extends CreativeWork {
  headline?: string;
  audio?: MusicGroup;
}

/** Social media or network post */
interface SocialMediaPosting extends Article {
  speechToDate?: number;
  video?: VideoObject;
}

/** Review of an item */
interface Review extends CreativeWork {
  reviewBody?: string;
  reviewRating?: Rating;
  itemReviewed?: Thing;
  rating?: Review;
}

/** Ratings in a number scale */
interface AggregateRating extends Thing {
  ratingCount?: number;
  bestRating?: number;
  worstRating?: number;
  ratingValue?: number;
}

/** A rating for an entity */
interface Rating extends Thing {
  author?: Organization | Person;
  bestRating?: number;
  ratingValue?: number;
  worstRating?: number;
}

/** A message */
interface Message extends CreativeWork {
  sender?: Organization | Person;
  recipient?: Organization | Person;
  dateSent?: string;
  dateRead?: string;
}

/** Digital content: images, audio, video, etc */
interface MediaObject extends CreativeWork {
  contentSize?: string;
  contentUrl?: string;
  uploadDate?: string;
  encoding?: string;
  duration?: string;
  bitrate?: string;
}

/** An image file */
interface ImageObject extends MediaObject {
  caption?: string | TextObject;
  exifData?: string;
  representativeOfPage?: boolean;
}

/** A music audio file */
interface AudioObject extends MediaObject {
  transcript?: string;
  embedUrl?: string;
}

/** A video file and some details */
interface VideoObject extends MediaObject {
  caption?: string | TextObject;
  videoFrameSize?: string;
  videoQuality?: string;
  embedUrl?: string;
  /** Person appearing in video */
  actor?: Person;
  /** Director of video */
  director?: Person;
  /** Music in video */
  musicBy?: Person | Organization;
  thumbnailUrl?: string;
}

/** Software as code */
interface SoftwareSourceCode extends CreativeWork {
  runtime?: string;
  targetProduct?: Product;
  programmingLanguage?: ProgrammingLanguage | string;
  codeRepository?: string;
  codeSampleType?: string;
  dateCreated?: string;
  fixDays?: number;
}

/** An application */
interface SoftwareApplication extends CreativeWork {
  applicationCategory?: string;
  applicationSubCategory?: string;
  applicationSuite?: string;
  supportingData?: DataFeed;
  /** Available on platforms */
  availableOn?: Product;
  /** Cost */
  offers?: Offer | Offer[];
  /** File size */
  fileSize?: string;
}

/** Video game */
interface VideoGameApplication extends SoftwareApplication {
  cheatCode?: string;
  gameServer?: GameServer;
  genre?: string | CreativeWork;
  gameTip?: CreativeWork;
}

/** Movie, TV series, etc */
interface Movie extends CreativeWork {
  duration?: string;
  director?: Person;
  actor?: Person | Person[];
  trailer?: VideoObject;
  musicBy?: Person | Organization;
}

/** TV series */
interface TVSeries extends CreativeWork {
  actor?: Person[];
  director?: Person | Person[];
  episode?: Episode[];
  season?: VideoObject;
  numberOfSeasons?: number;
  numberOfEpisodes?: number;
}

/** Single episode of a series */
interface Episode extends CreativeWork {
  episodeNumber?: number;
  partOfSeason?: Season;
  partOfTVSeries?: TVSeries;
}

/** A block of music */
interface MusicComposition extends CreativeWork {
  musicArrangement?: MusicComposition;
  composer?: Organization | Person;
  firstPerformance?: Event;
  includedInComposition?: MusicComposition;
  iswcCode?: string;
  recordedAs?: MusicRecording;
  compositionAsWritten?: MusicComposition;
}

/** Recording of a music track */
interface MusicRecording extends CreativeWork {
  album?: MusicAlbum;
  byArtist?: MusicGroup;
  duration?: string;
  isrcCode?: string;
}

/** Music album */
interface MusicAlbum extends CreativeWork {
  albumProductionType?: string;
  albumReleaseType?: MusicAlbumReleaseType;
  byArtist?: MusicGroup;
  numTracks?: number;
  track?: MusicRecording | MusicRecording[];
}

type MusicAlbumReleaseType = 
  | "AlbumPremiere"
  | "AlbumRelease"
  | "BroadcastRelease"
  | "EP";

/** A music group: band, musician, etc */
interface MusicGroup extends CreativeWork {
  /** Music group member */
  member?: Organization | Person;
  /** Genre of the music */
  genre?: string;
}

/** Podcast series */
interface PodcastSeries extends CreativeWork {
  episode?: Episode[];
  numberOfEpisodes?: number;
  startDate?: string;
  endDate?: string;
}

/** How-to or recipe */
interface HowTo extends CreativeWork {
  step?: HowToStep | HowToStep[];
  supplies?: HowToSupply | HowToSupply[];
  tools?: HowToTool | HowToTool[];
  totalTime?: string;
  estimatedCost?: MonaryAmount;
}

/** Recipe for cooking */
interface Recipe extends HowTo {
  cookTime?: string;
  prepTime?: string;
  recipeYield?: number | string;
  ingredients?: string[];
 nutrition?: NutritionInformation;
  recipeCategory?: string;
  recipeCuisine?: string;
  suitableForDiet?: RestrictedDiet;
}

type RestrictedDiet = 
  | "DiabeticDiet"
  | "GlutenFreeDiet"
  | "HalalDiet"
  | "HinduDiet"
  | "KosherDiet"
  | "LowCalorieDiet"
  | "LowFatDiet"
  | "LowLactoseDiet"
  | "LowSaltDiet"
  | "VeganDiet"
  | "VegetarianDiet";

// =============================================================================
// Events
// =============================================================================

/** An event: conference, concert, festival, etc */
interface Event extends Thing {
  /** Event status: cancelled, postponed, etc */
  eventStatus?: EventStatusType;
  /** Start date */
  startDate?: string;
  /** End date */
  endDate?: string;
  /** Event is held */
  eventAttendanceMode?: EventAttendanceModeEnumeration;
  /** Event location */
  location?: Place | string;
  /** Performer */
  performer?: Organization | Person | Person[];
  /** Organization */
  organizer?: Organization | Person;
  /** Duration of event */
  duration?: string;
  /** Url to offer */
  offers?: Offer | Offer[];
  /** Previous event */
  previousEvent?: Event;
  /** Subsequent event */
  nextEvent?: Event;
  /** Maximum capacity */
  maximumAttendeeCapacity?: number;
  /** Available seats */
  availableSeat?: number;
  /** Typical age range */
  typicalAgeRange?: string;
  /** Language */
  inLanguage?: string;
  /** Previous start */
  previousStartDate?: string;
  /** Event is for */
  attendee?: Organization | Person | Person[];
  /** Maximum physical attendee capacity */
  maximumPhysicalAttendeeCapacity?: number;
  /** Maximum attendees */
  maximumAttendees?: number;
}

type EventStatusType = 
  | "http://schema.org/EventCancelled"
  | "http://schema.org/EventMovedOnline"
  | "http://schema.org/EventPostponed"
  | "http://schema.org/EventRescheduled"
  | "http://schema.org/EventScheduled";

type EventAttendanceModeEnumeration = 
  | "http://schema.org/OfflineEventAttendanceMode"
  | "http://schema.org/OnlineEventAttendanceMode"
  | "http://schema.org/MixedEventAttendanceMode";

/** Course, like educational */
interface Course extends CreativeWork {
  courseCode?: string;
  courseMinimumAttendance?: CourseInstance;
  coursePrereqs?: Course | string;
  hasCourseInstance?: CourseInstance[];
  numberOfCredits?: number;
  professionalCategory?: string;
  requiresCompletion?: string;
}

/** Instance of a course */
interface CourseInstance extends Event {
  courseMode?: string;
  courseWorkload?: string;
  instructor?: Person;
}

/** An event on a schedule */
interface ScheduledEvent extends Event {
  /** Scheduled time */
  startDate?: string;
  /** End date */
  endDate?: string;
}

/** Publication of a book, etc */
interface PublicationEvent extends Event {
  /** If free */
  publishedOn?: BroadcastEvent;
}

/** Broadcast of radio/TV */
interface BroadcastEvent extends Event {
  /** Broadcast to be on */
  isBroadcastOf?: BroadcastService;
  /** Video format */
  videoFormat?: string;
}

/** Broadcast channel/radio station */
interface BroadcastService extends Thing {
  /** Name */
  name?: string;
  /** Organization */
  provider?: Organization | Person;
  /** Broadcast feed */
  broadcastFeed?: string;
}

// =============================================================================
// Organization, Person, and Place types
// =============================================================================

/** A group of people or orgs */
interface Organization extends Thing {
  /** Legal name */
  legalName?: string;
  /** URL of an image */
  logo?: string | ImageObject;
  /** The founding area */
  foundingLocation?: Place;
  /** Member of organization */
  member?: Organization | Person;
  /** Members */
  memberOf?: Organization | ProgramMembership;
  /** Number of members */
  numberOfMembers?: number;
  /** Fields of activity */
  areaServed?: Place | string | AdministrativeArea;
  /** Available service */
  availableService?: string;
  /** Brand */
  brand?: Brand | Organization;
  /** Contact details */
  contactPoint?: ContactPoint | ContactPoint[];
  /** Alumni */
  alumni?: Person[];
  /** Awards */
  award?: string;
  /** Email */
  email?: string;
  /** Employees */
  employee?: Person[];
  /** Founders */
  founder?: Person;
  /** Founding date */
  foundingDate?: string;
  /** Has POS */
  hasPOS?: Place;
  /** Keywords */
  keyword?: string;
  /** Known awards */
  knowsAbout?: string | Thing;
  /** Knows language */
  knowsLanguage?: string | Language;
  /** Location */
  location?: Place | PostalAddress | string;
  /** Doing business as */
  dba?: string;
  /** Parent org */
  parentOrganization?: Organization;
  /** Imported from */
  makesOffer?: Offer;
  /** Isic V4 */
  isicV4?: string;
  /** Same as */
  sameAs?: string;
  /** Tel and fax numbers */
  telephone?: string;
  faxNumber?: string;
  /** URL of sub org */
  subOrganization?: Organization;
}

/** Corporation, government, etc */
interface Corporation extends Organization {
  tickerSymbol?: string;
}

/** Government organization or orgaization type */
interface GovernmentOrganization extends Organization {
}

/** Non-profit organization */
interface NonProfitOrganization extends Organization {
  /** Registration number */
  registrationNumber?: string;
}

/** An airline company */
interface Airline extends Organization {
  iataCode?: string;
  icaoCode?: string;
}

/** An organization that provides sports teams */
interface SportsTeam extends Organization {
  athlete?: Person | Person[];
}

/** A public transport: train, bus, etc */
interface PublicTransport extends Organization {
  /** Transport type identifier */
  additionalType?: string;
  /** Route served */
  servesOnLine?: Route;
}

/** A local business */
interface LocalBusiness extends Organization {
  /** Areas served */
  areaServed?: Place;
  /** Location */
  location?: Place | PostalAddress;
  /** Opening hours */
  openingHoursSpecification?: OpeningHoursSpecification;
  /** Price range */
  priceRange?: string;
  /** Has map */
  hasMap?: string;
}

/** A restaurant */
interface Restaurant extends LocalBusiness {
  servesCuisine?: string;
  menu?: string | MenuItem;
  hasMenuSection?: MenuSection;
}

/** Government office */
interface GovernmentOffice extends LocalBusiness {
}

/** A store/retail */
interface Store extends LocalBusiness {
  /** Opening hours */
  openingHoursSpecification?: OpeningHoursSpecification;
}

/** An office: work office */
interface OfficeEquipmentStore extends Store {
}

/** A financial organization/service */
interface FinancialProduct extends Product {
  /** Annual percentage rate */
  annualPercentageRate?: number | QuantitativeValue;
  /** Fees and comm */
  feesAndCommissionsSpecification?: string;
  /** Interest rate */
  interestRate?: number | QuantitativeValue;
}

/** An account at bank/union */
interface BankAccount extends FinancialProduct {
  /** Account type */
  accountAllowed?: string;
  /** Minimum balance */
  accountMinimumBalance?: number | QuantitativeValue;
  /** Account requirements */
  accountRequirements?: string;
  /** Overdraft terms */
  overdraftFeesAndCommissions?: string;
}

/** Loan/credit */
interface LoanOrCredit extends FinancialProduct {
  /** Amount borrowed */
  amount?: number | MonetaryAmount | PriceSpecification;
  /** Required credit history */
  creditScoreRequirement?: number;
  /** Credit history requirement */
  requiredCreditScore?: number;
  /** Loan term */
  loanTerm?: QuantitativeValue;
  /** Loan type */
  loanType?: string;
  /** Amount owed */
  amountDue?: number | MonetaryAmount;
  /** Number of payments */
  numberOfLoanPayments?: number;
}

/** Payment card */
interface PaymentCard extends FinancialProduct {
  /** Card issuer */
  cardIssuer?: Organization;
  /** Card number */
  cardNumber?: string;
  /** Cash back */
  cashBack?: number | MonetaryAmount;
  /** Card merchant */
  merchantCategory?: string;
  /** Annual fee */
  annualFee?: number | MonetaryAmount;
  /** APR for cash advance */
  cashAdvanceFee?: number | MonetaryAmount;
  /** Interest on cash advances */
  cashAdvanceInterestRate?: number | QuantitativeValue;
  /** Minimum payment */
  minimumPayment?: number | MonetaryAmount;
}

/** Investment fund */
interface InvestmentFund extends FinancialProduct {
  /** Fees */
  feesAndCommissionsSpecification?: string;
}

/** Currency: dollars, euros, etc */
interface CurrencyAmount extends Thing {
  /** Numeric value */
  amount?: number;
  /** Currency code */
  currency?: string;
}

/** A person (human) */
interface Person extends Thing {
  /** Additional name */
  additionalName?: string;
  /** Address */
  address?: PostalAddress | string;
  /** Affiliation */
  affiliation?: Organization[];
  /** Alternate names */
  alternateName?: string;
  /** Awards */
  award?: string;
  /** Best rating */
  bestRating?: number;
  /** Birth date */
  birthDate?: string;
  birthPlace?: Place;
  /** Brand */
  brand?: Brand | Organization;
  /** Call sign */
  callSign?: string;
  /** Children */
  children?: Person[];
  /** Colleague */
  colleague?: Person | Person[];
  /** Contact point */
  contactPoint?: ContactPoint;
  /** Date of death */
  deathDate?: string;
  deathPlace?: Place;
  /** Email */
  email?: string;
  /** Family name */
  familyName?: string;
  /** Fax number */
  faxNumber?: string;
  /** Follows */
  follows?: Person[];
  /** Gender */
  gender?: string;
  /** Given name */
  givenName?: string;
  /** Globally unique identifier */
  identifier?: string;
  /** Job title */
  jobTitle?: string;
  /** Knows */
  knows?: Person[];
  /** Knows about */
  knowsAbout?: string | Thing;
  /** Languages spoken */
  knowsLanguage?: string | Language;
  /** Memberships */
  memberOf?: Organization | ProgramMembership;
  /** Nationality */
  nationality?: Country | string;
  /** Email */
  owns?: Product | Product[];
  /** Past projects */
  memberOf?: Organization;
  /** Performer in */
  performerIn?: Event;
  /** Profanity */
  profession?: string;
  /** Property */
  property?: string;
  /** Related link */
  relatedTo?: Person[];
  /** Relative */
  relative?: Person[];
  /** Same as */
  sameAs?: string;
  /** School */
  alumni?: Person[];
  /** Seeking */
  seeks?: Product | Demand;
  /** Sibling */
  sibling?: Person[];
  /** Contact */
  sponsor?: Organization | string;
  /** Spouse */
  spouse?: Person;
  /** Sudden death */
  subpremise?: string;
  /** Tax ID */
  taxID?: string;
  /** Telephone */
  telephone?: string;
  /** Ticker */
  telReturnOrCallKey?: string;
  /** Updated */
  url?: string;
  /** Worth */
  weight?: number;
  /** Working for */
  worksFor?: Organization[];
}

/** A contact point for an organization */
interface ContactPoint extends Thing {
  /** Email */
  email?: string;
  /** Telephone */
  telephone?: string;
  /** For product */
  productSupported?: string | Product;
  /** Available times */
  availableHours?: OpeningHoursSpecification;
  /** Language */
  contactType?: string;
  /** Contact option */
  contactOption?: ContactPointOption;
  /** Email */
  email?: string;
  /** Phone type */
  telephone?: string;
}

/** A contact point option */
interface ContactPointOption extends Thing {
  /** This is the option for the contact */
  availableOn?: string;
  optionType?: string;
}

/** Brand value entity */
interface Brand extends Thing {
  /** Logo URL or ID */
  logo?: string | ImageObject;
  /** Review */
  aggregateRating?: AggregateRating;
}

/** Place: location, venue, etc */
interface Place extends Thing {
  /** Additional photos */
  additionalProperty?: PropertyValue;
  /** Address */
  address?: PostalAddress | string;
  /** Name */
  address?: PostalAddress;
  /** Map */
  hasMap?: string;
  /** Is an accepted payment */
  isAcceptingNewPatients?: boolean;
  /** Location */
  containedInPlace?: Place;
  /** Contains */
  containsPlace?: Place;
  /** Directions */
  directions?: string;
  /** Event */
  event?: Event;
  /** Latitude */
  latitude?: number | string;
  /** Longitude */
  longitude?: number | string;
  /** Map */
  maximumAttendeeCapacity?: number;
  /** Opening hours */
  openingHoursSpecification?: OpeningHoursSpecification[];
  /** Photo */
  photo?: ImageObject | Photograph;
  /** Reviews */
  review?: Review | Review[];
  /** Same as */
  sameAs?: string;
  /** Reserved seating */
  seatingCapacity?: number;
  /** Map */
  smap?: string;
  /** Relevant photos */
  subjectOf?: Event | CreativeWork;
  /** URL */
  url?: string;
}

/** An accommodation: hotel, etc */
interface Accommodation extends Place {
  /** Number of rooms */
  numberOfRooms?: number | QuantitativeValue;
  /** Permitted usage */
  permittedUsage?: string;
  /** Smoking allowed */
  smokingAllowed?: boolean;
  /** Bed info */
  bed?: BedDetails;
  /** Occupancy */
  occupancy?: QuantitativeValue;
}

/** An accommodation type */
interface Apartment extends Accommodation {
  /** Occupancy */
  occupancy?: QuantitativeValue;
}

/** An accommodation property */
interface CampingPitch extends Accommodation {
}

/** A house: single family home */
interface SingleFamilyResidence extends Accommodation {
  /** Number of rooms */
  numberOfRooms?: number;
  /** Occupancy */
  occupancy?: QuantitativeValue;
}

/** Hotel */
interface Hotel extends LodgingBusiness {
  /** Star rating */
  starRating?: Rating;
}

/** Bed and breakfast */
interface BedAndBreakfast extends LodgingBusiness {
  /** Has restaurant */
  hasResturantMenu?: MenuItem | MenuItem[];
}

/** A vacation rental */
interface VacationRental extends Accommodation {
  amenityFeature?: LocationFeatureSpecification;
}

/** A building */
interface Building extends Place {
  /** Number of floors */
  numberOfFloors?: number;
  /** Parking */
  parking?: string;
}

/** A public building */
interface PublicBuilding extends Building {
}

/** An airport */
interface Airport extends Place {
  iataCode?: string;
  icaoCode?: string;
}

/** Body of water */
interface BodyOfWater extends Place {
}

/** Beach */
interface Beach extends Place {
  /** Tourist type */
  touristType?: string;
}

/** A bridge */
interface Bridge extends Place {
}

/** Cemetery */
interface Cemetery extends Place {
}

/** A city */
interface City extends Place {
}

type City = Place;

/** A continent */
interface Continent extends Place {
}

/** A country */
interface Country extends Place {
}

/** A dam */
interface Dam extends Place {
}

/** A building or area */
interface EducationalOrganization extends Organization {
  /** Accepting new students */
  acceptsAdmissionRequests?: string;
  /** Program */
  course?: Course | Course[];
  /** Program offered */
  program?: Course;
  /** Degrees */
  degree?: EducationalOccupationalProgram;
  /** Minimum requirement */
  minimumEnrollment?: number;
}

/** A college/university */
interface CollegeOrUniversity extends EducationalOrganization {
}

/** Elementary school */
interface ElementarySchool extends EducationalOrganization {
}

/** High school */
interface HighSchool extends EducationalOrganization {
}

/** Primary school */
interface PrimarySchool extends EducationalOrganization {
}

/** A playground */
interface Playground extends Place {
}

/** A park */
interface Park extends Place {
}

/** A religious place */
interface ReligiousPlace extends Place {
}

/** A cemetery */
interface CemeteryOrCrematorium extends Place {
}

/** A scenic view */
interface ScenicViewpoint extends Place {
}

/** Stadium or sports venue */
interface SportsActivityLocation extends Place {
}

/** A subway station */
interface SubwayStation extends Place {
}

/** A taxi stand */
interface TaxiStand extends Place {
}

/** A tourist attraction */
interface TouristAttraction extends Place {
  /** Tourist type */
  touristType?: string;
}

/** A tour */
interface TouristDestination extends Place {
  /** Includes description of a thing */
  doesNotInclude?: string | Thing;
  includes?: string | Thing;
}

/** Administrative area: state, province, etc */
interface AdministrativeArea extends Place {
  /** Name of admin area */
  name?: string;
}

/** Borough/gov block */
interface AdministrativeArea = Place | City | Country | State;

/** Geo coordinates */
interface GeoCoordinates extends Thing {
  address?: PostalAddress | string;
  addressCountry?: string;
  elevation?: number | string;
  latitude?: number | string;
  longitude?: number | string;
  postalCode?: string;
}

/** A geo shape: polygon, circle, etc */
interface GeoShape extends Thing {
  address?: PostalAddress | string;
  addressCountry?: string;
  box?: string;
  circle?: string;
  elevation?: number | string;
  line?: string;
  polygon?: string;
  postalCode?: string;
}

/** Opening hours */
interface OpeningHoursSpecification extends Thing {
  /** Day of week */
  dayOfWeek?: DayOfWeek | string;
  /** Opens at */
  opens?: string;
  /** Closes at */
  closes?: string;
  /** Valid from */
  validFrom?: string;
  /** Valid through */
  validThrough?: string;
}

/** Day of week enumeration */
type DayOfWeek = 
  | "http://schema.org/Friday"
  | "http://schema.org/Monday"
  | "http://schema.org/Saturday"
  | "http://schema.org/Sunday"
  | "http://schema.org/Thursday"
  | "http://schema.org/Tuesday"
  | "http://schema.org/Wednesday";

/** A location feature on a map */
interface LocationFeatureSpecification extends Thing {
  /** Name */
  name?: string;
  /** Option value */
  value?: string | number | boolean;
}

/** A Postal address */
interface PostalAddress extends Thing {
  /** Address country */
  addressCountry?: Country | string;
  /** Address locality: city */
  addressLocality?: string;
  /** Address region: state/province */
  addressRegion?: string;
  /** Post office box number */
  postOfficeBoxNumber?: string;
  /** Postal code */
  postalCode?: string;
  /** Street address */
  streetAddress?: string;
  /** Address as string */
  name?: string;
  /** Street number */
  streetNumber?: string;
  /** Floor number */
  floorLevel?: string;
  /** Premise name */
  premise?: string;
}

/** State */
interface State extends Place {
}

/** A map */
interface Map extends CreativeWork {
  /** If map */
  mapType?: string;
}

// =============================================================================

// =============================================================================
// PRODUCTS & E-COMMERCE
// =============================================================================

/** A product: item for sale */
interface Product extends Thing {
  /** Additional product attribute */
  additionalProperty?: PropertyValue;
  /** Aggregate rating */
  aggregateRating?: AggregateRating;
  /** Is an accessory */
  isAccessoryOrSparePartFor?: Product;
  /** Is related product */
  isRelatedTo?: Product;
  /** Is similar */
  isSimilarTo?: Product;
  /** Is product bundle */
  isBundle?: boolean;
  /** Item condition */
  itemCondition?: OfferItemCondition;
  /** Manufacturer */
  manufacturer?: Organization;
  /** Model */
  model?: ProductModel | string;
  /** Product name */
  name?: string;
  /** Offers */
  offers?: Offer | Offer[];
  /** Product OUI */
  productID?: string;
  /** Production date */
  productionDate?: string;
  /** Purchase date */
  purchaseDate?: string;
  /** Release date */
  releaseDate?: string;
  /** Review */
  review?: Review | Review[];
  /** SKU */
  sku?: string | number;
  /** GTIN */
  gtin?: string;
  /** Global Trade Item Number */
  gtin12?: string;
  gtin13?: string;
  gtin14?: string;
  gtin8?: string;
  /** NPA */
  npan?: string;
  /** Color */
  color?: string;
  /** Depth */
  depth?: Distance | QuantifiedValue;
  /** Height */
  height?: Distance | QuantifiedValue;
  /** Width */
  width?: Distance | QuantifiedValue;
  /** Weight */
  weight?: QuantifiedValue;
  /** Logo */
  logo?: string;
  /** URL */
  url?: string;
}

/** Product model information */
interface ProductModel extends Product {
  /** Is product variant */
  isVariantOf?: ProductModel;
  /** Predecessor of */
  predecessorOf?: ProductModel;
  /** Successor of */
  successorOf?: ProductModel;
  /** Related model */
  relatedTo?: ProductModel;
}

/** An offer to sell */
interface Offer extends Thing {
  /** Accepted payment method */
  acceptedPaymentMethod?: PaymentMethod;
  /** Additional property */
  additionalProperty?: PropertyValue;
  /** Add on */
  addOn?: Offer;
  /** Aggregate rating */
  aggregateRating?: AggregateRating;
  /** Availability */
  availability?: ItemAvailability | string;
  /** When available */
  availabilityEnds?: string;
  /** Available from */
  availableFrom?: string;
  /** Available through */
  availableThrough?: string;
  /** Business function */
  businessFunction?: BusinessFunction;
  /** Delivery method */
  deliveryMethod?: DeliveryMethod;
  /** Inventory level */
  inventoryLevel?: QuantitativeValue;
  /** Item condition */
  itemCondition?: OfferItemCondition;
  /** Item offered */
  itemOffered?: Product | Service;
  /** Earliest delivery */
  earliestDelivery?: string;
  /** Price */
  price?: number | string;
  /** Price currency */
  priceCurrency?: string;
  /** Price specification */
  priceSpecification?: PriceSpecification;
  /** Valid from */
  validFrom?: string;
  /** Valid through */
  validThrough?: string;
  /** High price */
  highPrice?: number | string;
  /** Low price */
  lowPrice?: number | string;
  /** Price type */
  priceType?: string;
  /** The amount */
  unitPrice?: QuantitativeValue;
  /** URL of the offer */
  url?: string;
  /** Warranty */
  warranty?: WarrantyPromise;
}

/** An offer for employment */
interface JobPosting extends Thing {
  /** Special commitments */
  specialCommitments?: string;
  /** Date job was posted */
  datePosted?: string;
  /** Free text */
  textual?: string;
  /** Base salary */
  baseSalary?: number | MonetaryAmount | PriceSpecification;
  /** Direct apply */
  directApplication?: boolean;
  /** Employment type */
  employmentType?: string;
  /** Hiring organization */
  hiringOrganization?: Organization;
  /** Industry */
  industry?: string;
  /** Job location */
  jobLocation?: Place;
  /** Location type */
  jobLocationType?: string;
  /** Next posting date */
  nextPosting?: string;
  /** occupational */
  occupationalCategory?: string | CategoryCode;
  /** Qualifications */
  qualifications?: string;
  /** related to */
  relatedTo?: JobPosting;
  /** Responsibilities */
  responsibilities?: string;
  /** Relevant occupation */
  relevantOccupation?: string;
  /** Security clearance required */
  securityClearanceRequirement?: string;
  /** Sensory info required */
  sensoryDetailRequirement?: string;
  /** Skills */
  skills?: string | DefinedTerm;
  /** Work for */
  workHours?: string;
}

/** A product or service from a business */
interface ItemAvailability = 
  | "http://schema.org/BackOrder"
  | "http://schema.org/Discontinued"
  | "http://schema.org/InStock"
  | "http://schema.org/InStoreOnly"
  | "http://schema.org/LimitedAvailability"
  | "http://schema.org/OnlineOnly"
  | "http://schema.org/OutOfStock"
  | "http://schema.org/PreOrder"
  | "http://schema.org/SoldOut"
  | "http://schema.org/Unavailable";

type OfferItemCondition = 
  | "http://schema.org/ConditionType"
  | "http://schema.org/DiscontinuedCondition"
  | "http://schema.org/NewCondition"
  | "http://schema.org/RefurbishedCondition"
  | "http://schema.org/UsedCondition";

type ItemAvailability = OfferItemCondition;

/** Price specification */
interface PriceSpecification extends Thing {
  /** Price */
  price?: number | string;
  /** Price currency */
  priceCurrency?: string;
  /** Valid from */
  validFrom?: string;
  /** Valid through */
  validThrough?: string;
  /** Value added tax */
  valueAddedTaxIncluded?: boolean;
  /** Minimum price */
  minPrice?: number;
  /** Maximum price */
  maxPrice?: number;
}

/** Monetary amount */
interface MonetaryAmount extends PriceSpecification {
  /** Currency code */
  currency?: string;
  /** Maximum price */
  maxPrice?: number;
  /** Minimum price */
  minPrice?: number;
}

/** Quantitative value with unit */
interface QuantitativeValue extends Thing {
  /** Max value */
  maxValue?: number;
  /** Min value */
  minValue?: number;
  /** Numerical value */
  value?: number | string;
  /** Unit code */
  unitCode?: string;
  /** Reference value */
  valueReference?: QuantitativeValue | string;
}

/** A measurement */
interface MeasurementType extends Thing {
  /** Measurement */
  measurement?: QuantitativeValue;
  /** Measurement method */
  measurementMethod?: string;
  /** Measurement system */
  measurementSystem?: string;
  /** Type of measurement */
  measurementType?: string;
}

/** Distance measurement */
interface Distance extends MeasurementType {
}

/** Weight measurement */
interface Weight extends MeasurementType {
}

/** A service: professional services like banking, etc */
interface Service extends Thing {
  /** Service provider */
  provider?: Organization | Person;
  /** Production registration */
  providerMobility?: string;
  /** Area served */
  areaServed?: Place | string | AdministrativeArea;
  /** Available service */
  availableChannel?: ServiceChannel;
  /** Consumer on */
  category?: CategoryCode | string;
  /** Is credential */
  hasCredential?: string | DefinedTerm;
  /** Is related */
  isSimilarTo?: Product;
  /** Logo */
  logo?: ImageObject | string;
  /** Official rating */
  officialRating?: Rating;
  /** Offers */
  offers?: Offer | Offer[];
  /** Produces */
  produces?: Thing | Product;
  /** Provider type */
  providerType?: string;
  /** Review */
  review?: Review | Review[];
  /** Same as */
  sameAs?: string;
  /** Service output */
  serviceOutput?: Thing;
  /** Type of service */
  serviceType?: string;
  /** URL */
  url?: string;
}

/** Phone, web, etc */
interface ServiceChannel extends Thing {
  /** Availability */
  availabilityEnds?: string;
  /** Available from */
  availableFrom?: string;
  /** Provider */
  provider?: Organization | Person;
  /** Service provided */
  serves?: Product;
  /** Time required */
  timeRequired?: string;
  /** URL */
  url?: string;
}

/** Professional service */
interface ProfessionalService extends LocalBusiness {
}

/** A financial service */
interface FinancialProduct extends Product {
}

/** Accountancy */
interface AccountingService extends ProfessionalService {
}

/** A legal service */
interface LegalService extends ProfessionalService {
  /** Jurisdiction */
  jurisdiction?: Place | string;
}

/** A real estate agent service */
interface RealEstateAgent extends ProfessionalService {
}

/** A radio service */
interface RadioService extends Service {
}

/** A government service */
interface GovernmentService extends Service {
  /** Service provided by */
  serviceOwner?: Organization;
  /** Service provided to */
  serviceRecipient?: Organization | Person;
}

/** Cable/satellite service */
interface CableOrSatelliteService extends Service {
}

/** An installment for payment */
interface PaymentChargeSpecification extends PriceSpecification {
  /** Payment method */
  allowedPaymentMethod?: PaymentMethod;
  /** Required payment method */
  requiredPaymentMethod?: PaymentMethod;
}

/** Delivery method */
interface DeliveryMethod extends Enumeration {
}

/** Method of payment */
interface PaymentMethod extends Enumeration {
}

/** A delivery method for a parcel */
interface ParcelService extends DeliveryMethod {
}

/** Delivery method */
interface DeliveryMode extends Enumeration {
}

/** Billing method for products */
interface PaymentCard extends FinancialProduct,
  DeliveryMethod {
  cardIssuer?: Organization;
}

/** Credit card */
type CreditCard = PaymentCard;

/** Enumeration class */
interface Enumeration extends Thing {
}

/** Business function */
interface BusinessFunction extends Enumeration {
}

/** Warranty promise */
interface WarrantyPromise extends Thing {
  /** Warranty duration */
  warrantyDuration?: Duration;
  /** Warranty type */
  warrantyType?: string;
}

/** Duration */
interface Duration extends Quantity {
  duration?: string;
}

/** A property-value pair */
interface PropertyValue extends Thing {
  /** Property ID */
  propertyID?: string;
  /** Value */
  value?: string | number | boolean;
  /** Value reference */
  valueReference?: PropertyValue | string;
}

/** Defined term */
interface DefinedTerm extends Thing {
  /** Term code */
  termCode?: string;
}

/** Category code */
interface CategoryCode extends DefinedTerm {
  codeValue?: string;
}

/** A quantity */
interface Quantity extends Thing {
}

/** A structured value */
interface StructuredValue extends Thing {
}

/** A nutritional info */
interface NutritionInformation extends Thing {
  /** Serving size */
  servingSize?: string;
  /** Calories */
  calories?: Energy;
  /** Carbohydrate content */
  carbohydrateContent?: Mass;
  /** Cholesterol content */
  cholesterolContent?: Mass;
  /** Fat content */
  fatContent?: Mass;
  /** Fiber content */
  fiberContent?: Mass;
  /** Protein content */
  proteinContent?: Mass;
  /** Sodium content */
  sodiumContent?: Mass;
  /** Sugar content */
  sugarContent?: Mass;
  /** Trans fat */
  transFatContent?: Mass;
}

/** Energy quantity */
interface Energy extends Quantity {
}

/** Mass quantity */
interface Mass extends Quantity {
}

/** Energy unit */
type Energy = Quantity;

/** A calorie */
type Calorie = Energy;

/** Gram quantity */
type Gram = Mass;

/** Unit price specification */
interface UnitPriceSpecification extends PriceSpecification {
  /** Price per unit */
  pricePerUnit?: number;
  /** Unit code */
  unitCode?: string;
}

// =============================================================================
// DATA TYPES
// =============================================================================

/** Boolean */
type Boolean = boolean;

/** Date/January 1, 2020 */
type Date = string;

/** Date/Time: 2020-01-01T12:00:00Z */
type DateTime = string;

/** Time: 12:00:00Z */
type Time = string;

/** DateTime and Duration */
type Duration = string;

/** Phone number */
type PhoneNumber = string;

/** URL */
type URL = string;

/** Number */
type Number = number;

// =============================================================================
// MEDICAL TYPES
// =============================================================================

/** Drug/medicine */
interface Drug extends MedicalEntity {
  /** Active ingredient */
  activeIngredient?: string | DefinedTerm;
  /** Administration route */
  administrationRoute?: string;
  /** Allowed dosage */
  allowableUnlabeledDrugQuantity?: number;
  /** Available strength */
  availableStrength?: DrugStrength;
  /** Clinical drug */
  clinicalDrug?: ClinicalDrug;
  code?: CategoryCode;
  /** Clinical trial */
  clinicalTrial?: ClinicalTrial;
  /** Dosage form */
  dosageForm?: DrugClass;
  /** Dosage unit */
  dosageUnit?: DefinedTerm;
  /** Generic, brand names */
  isGeneric?: boolean;
  isAvailable?: boolean;
  /** Available as over the counter */
  isPrescriptionAuthorized?: boolean;
  /** Maximum intake */
  maximumIntake?: string;
  /** Drug form */
  drugClass?: DrugClass;
  /** Drug formulation */
  drugFormula?: string;
  /** Generic identifier */
  hasGenericForm?: Drug;
  /** Interacting drug */
  interactingDrug?: Drug;
  /** Legal category */
  legalStatus?: DrugClassification;
  /** Manufacturer */
  manufacturer?: Organization;
  /** Markings (letters/numbers) */
  markingImage?: ImageObject;
  /** Active ingredient */
  activeIngredient?: string;
  /** Dose schedule */
  doseSchedule?: DoseSchedule;
  /** Drug status */
  drugWarning?: string;
}

/** Clinical drug content */
interface ClinicalDrug extends Drug {
  /** Drug name */
  drugName?: string;
  /** Strength */
  dosage?: DrugDosage;
  includes?: string | Food;
}

/** Drug class */
interface DrugClass extends MedicalEntity {
  /** Possible drug */
  possibleDrug?: Drug;
  /** Includes drug */
  includesDrug?: DrugClass;
  /** Drug class */
  classOfDevAlert?: Device;
}

/** Strength of a drug */
interface DrugStrength extends MedicalEntity {
  /** Active ingredient */
  activeIngredient?: string;
  /** Available at */
  availableIn?: AdministrativeArea;
  /** Strength */
  strengthUnit?: DefinedTerm;
  /** Strength value */
  strengthValue?: number;
}

/** Medical dose schedule */
interface DoseSchedule extends Thing {
  /** Dose */
  dose?: QuantitativeValue;
  /** Frequency */
  frequency?: string;
  /** Dose unit */
  doseUnit?: DefinedTerm;
  /** How to take */
  guidance?: string;
  /** Time to take */
  releaseDate?: string;
}

/** Medical entity */
interface MedicalEntity extends Thing {
  /** Relevant specialty */
  relevantSpecialty?: string;
  /** Medical code */
  code?: MedicalCode;
  /** Guideline */
  guideline?: MedicalGuideline;
  /** Study */
  legalStatus?: MedicalEntity;
  /** Study */
  study?: MedicalStudy;
}

/** Medical code */
interface MedicalCode extends CategoryCode {
  /** Coding system */
  codingSystem?: string;
}

/** Medical guidelines */
interface MedicalGuideline extends MedicalEntity {
  /** Guideline subject */
  guidelineSubject?: MedicalEntity;
  /** Guideline date */
  dateModified?: string;
  /** Guideline topic */
  guidelineTopic?: MedicalGuideline;
  /** Evidence origin */
  evidenceOrigin?: string;
  /** Recommendation strength */
  recommendationStrength?: string;
}

/** Medical study */
interface MedicalStudy extends MedicalEntity {
  /** Study location */
  studyLocation?: string;
  /** Study phase */
  studyPhase?: string;
  /** Study results */
  studyResults?: string;
  /** Status */
  status?: string;
  /** Study type */
  studyType?: string;
  /** Sponsors */
  sponsor?: Organization;
  /** Methods */
  measurement?: MedicalObservation;
}

/** A medical condition */
interface MedicalCondition extends MedicalEntity {
  /** Associated anatomy */
  associatedAnatomy?: AnatomicalStructure | Anatomy;
  /** Cause */
  cause?: MedicalCause | string;
  /** Condition of this condition */
  differentialDiagnosis?: DDxElement;
  /** Risk factor */
  possibleTreatment?: MedicalTherapy;
  /** Possible treatment */
  primaryPrevention?: MedicalTherapy;
  /** Secondary prevention */
  secondaryPrevention?: MedicalTherapy;
  /** Signs and symptoms */
  signOrSymptom?: MedicalSignOrSymptom;
  /** Stage */
  stage?: MedicalConditionStage;
  /** Status */
  status?: MedicalConditionStatus;
  /** Subtype */
  subType?: string;
  /** Typical test */
  typicalTest?: MedicalTest;
}

/** Body part */
interface AnatomicalStructure extends MedicalEntity {
  /** Connected to */
  connectedTo?: AnatomicalStructure;
  /** Muscles */
  dialect?: string;
  /** Located in */
  locatedIn?: Anatomy;
  /** Location */
  location?: AnatomicalStructure;
  /** Visually present */
  image?: ImageObject;
}

/** Body system */
interface Anatomy extends MedicalEntity {
  associatedPathophysiology?: string;
  /** Related conditions */
  relatedCondition?: MedicalCondition;
  /** Related body part */
  relatedTo?: Anatomy;
}

/** Medical sign/symptom */
interface MedicalSignOrSymptom extends MedicalEntity {
  /** Possible cause */
  possibleCause?: DDxElement;
  /** Risk factor */
  riskFactor?: MedicalRiskFactor;
  /** Sign of a condition */
  signOrSymptom?: MedicalSignOrSymptom;
  /** Identifying info */
  Identifying?: string;
}

/** Medical observation */
interface MedicalObservation extends MedicalEntity {
  /** Normal range */
  normalRange?: string;
  /** Significance */
  significance?: string;
  /** Observation method */
  observationMethod?: string;
  /** Subject */
  subject?: string;
}

/** Medical test */
interface MedicalTest extends MedicalEntity {
  /** Device used */
  usesDevice?: MedicalDevice;
  /** Test results */
  normalRange?: MedicalReference,
  /** Normal value */
  signOrSymptom?: MedicalEntity;
}

/** A medical device */
interface MedicalDevice extends MedicalEntity {
  /** Device code */
  code?: MedicalCode;
  /** Contraindication */
  contraindication?: string;
  /** Pre-market approval */
  preMarket?: boolean;
  /** Procedure */
  possibleProcedure?: MedicalProcedure;
  /** Primary safety */
  primarySafety?: string;
  /** Product code */
  productCode?: string;
  /** Safety information */
  safetyInformation?: string;
  /** Status */
  status?: MedicalDeviceStatus;
  /** Usage */
  usage?: string;
}

/** Medical therapy/treatment */
interface MedicalTherapy extends MedicalEntity {
  /** Possible adverse effect */
  possibleAdverseEffect?: MedicalEntity;
  /** Treatment intensity */
  intensity?: string;
  /** Form of therapy */
  therapyType?: string;
}

/** A medical procedure */
interface MedicalProcedure extends MedicalEntity {
  /** Procedure body location */
  bodyLocation?: string;
  /** Folate */
  followup?: string;
  /** How performed */
  howPerformed?: string;
  /** Preparation */
  preparation?: string;
  /** Status */
  status?: MedicalProcedureType;
}

/** Medical status */
type MedicalDeviceStatus = 
  | "http://schema.org/Active"
  | "http://schema.org/Inactive"
  | "http://schema.org/Recalled";

type MedicalProcedureType = 
  | "http://schema.org/Diagnostic"
  | "http://schema.org/ Therapeutic";

type MedicalConditionStatus = 
  | "http://schema.org/Active"
  | "http://schema.org/Remission"
  | "http://schema.org/Resolved";

/** Medical risk factor */
interface MedicalRiskFactor extends MedicalEntity {
  /** Increases risk of */
  increasesRiskOf?: MedicalCondition;
}

type DDxElement = thing;

// =============================================================================
// ADDITIONAL SCHEMA TYPES
// =============================================================================

/** Answer to a question */
interface QAPage extends QAPage {
  /** Answer count */
  answerCount?: number;
  /** Question pages */
  questions?: Question[];
  upvotedAnswers?: Answer;
}

/** Question and answer page */
interface FAQPage extends QAPage {
}

type QAPage = WebPage;

// =============================================================================

// =============================================================================
// FAQPage = WebPage {
// =============================================================================
// Additional types for products and services:
// =============================================================================

/** Type of reservation */
type ReservationType = 
  | "http://schema.org/Reservation"
  | "http://schema.org/Address"
  | "http://schema.org/BoatReservation"
  | "http://schema.org/BusReservation"
  | "http://schema.org/EventReservation"
  | "http://schema.org/FlightReservation"
  | "http://schema.org/FoodEstablishmentReservation"
  | "http://schema.org/LodgingReservation"
  | "http://schema.org/RentalCarReservation"
  | "http://schema.org/ReservationPackage"
  | "http://schema.org/TaxiReservation";

/** Ticket for event */
interface Reservation extends Thing {
  /** Booking agent */
  bookingAgent?: Organization | Person;
  /** Booking time */
  bookingTime?: string;
  /** Reserved for */
  bookingReservation?: Reservation;
  /** Modified time */
  dateModified?: string;
  /** Modified by */
  modifiedTime?: string;
  /** Cancellation */
  cancellationDeadline?: string;
  /** Confirmation number */
  confirmationNumber?: string;
  /** Currency */
  currency?: string;
  /** Reservation for */
  reservationFor?: Thing;
  /** Reservation ID */
  reservationId?: string;
  /** Reservation status */
  reservationStatus?: ReservationStatusType;
  /** Total price */
  totalPrice?: number | string | PriceSpecification;
  /** Under name */
  underName?: Person | Organization;
}

/** Reservation status */
type ReservationStatusType = 
  | "http://schema.org/ReservationCancelled"
  | "http://schema.org/ReservationConfirmed"
  | "http://schema.org/ReservationHold"
  | "http://schema.org/ReservationPending";

/** Flight reservation */
interface FlightReservation extends Reservation {
  /** Boarding group */
  boardingGroup?: string;
  /** Flight */
  passengerPriorityStatus?: string;
  /** Passengers */
  passengerForGrouping?: Person;
  /** Security line */
  securityWait?: number;
  /** Terminal */
  terminal?: string;
  /** Gate */
  gate?: string;
}

/** Lodging reservation */
interface LodgingReservation extends Reservation {
  /** Checkin time */
  checkinTime?: string;
  /** Checkout time */
  checkoutTime?: string;
  /** Lodging unit */
  lodgingUnitDescription?: string;
  /** Lodging unit */
  lodgingUnitType?: string;
  /** Number of guests */
  numGuests?: number;
}

/** Order */
interface Order extends Thing {
  /** Accepted offer */
  acceptedOffer?: Offer;
  /** Associated with order */
  associatedWith?: Order | Product;
  /** Billing address */
  billingAddress?: PostalAddress;
  /** Broker */
  broker?: Organization | Person;
  /** Confirmation number */
  confirmationNumber?: string;
  /** Customer */
  customer?: Organization | Person;
  /** Discount */
  discount?: number | string;
  /** Discount code */
  discountCode?: string;
  /** Is gift */
  isGift?: boolean;
  /** Fulfilled by */
  orderDate?: string;
  /** Items ordered */
  orderItem?: OrderItem [];
  /** Order delivered */
  orderDelivery?: ParcelDelivery;
  /** Order number */
  orderNumber?: string;
  /** Order status */
  orderStatus?: OrderStatus;
  /** Parts ship */
  partOfInvoice?: Invoice;
  /** Items in order */
  scheduledPayment?: string;
  /** Seller */
  seller?: Organization | Person;
  /** Total price */
  totalPaymentDue?: Number | MonetaryAmount;
}

/** Order item */
interface OrderItem extends Thing {
  /** Order item */
  orderDelivery?: ParcelDelivery;
  /** Order item ID */
  orderItemNumber?: string;
  /** Order item status */
  orderItemStatus?: OrderItemStatus;
  /** Order to fulfill */
  orderQuantity?: number;
  /** Order price */
  orderedItem?: Product | Service;
}

/** Payment status */
type OrderStatus = 
  | "http://schema.org/OrderCancelled"
  | "http://schema.org/OrderDelivered"
  | "http://schema.org/OrderInTransit"
  | "http://schema.org/OrderPaymentDue"
  | "http://schema.org/OrderPickupAvailable"
  | "http://schema.org/OrderProblem"
  | "http://schema.org/OrderProcessing"
  | "http://schema.org/OrderReturned";

type OrderItemStatus = 
  | "http://schema.org/OrderItemCancelled"
  | "http://schema.org/OrderItemDelivered"
  | "http://schema.org/OrderItemInTransit"
  | "http://schema.org/OrderItemLost"
  | "http://schema.org/OrderItemPaid"
  | "http://schema.org/OrderItemPickupAvailable"
  | "http://schema.org/OrderItemProblem"
  | "http://schema.org/OrderItemReturned"
  | "http://schema.org/OrderItemShipped";

/** Carrier/fulfiller */
interface ParcelDelivery extends Thing {
  /** Delivery company */
  deliveryAddress?: PostalAddress;
  /** Delivery date */
  deliveryDate?: string;
  /** Delivery time */
  deliveryTime?: string;
  /** Carrier */
  carrier?: Organization;
  /** Has tracking */
  hasTrackingNumber?: string;
  /** Destination */
  destination?: PostalAddress;
  /** Origin address */
  originAddress?: PostalAddress;
  /** Expected arrival */
  itemShipped?: Product;
  /** Tracking url */
  trackingUrl?: string;
}

/** Invoice for order */
interface Invoice extends Thing {
  /** Account number */
  accountNumber?: string;
  /** Billing period */
  billingPeriod?: string;
  /** References */
  broker?: Organization | Person;
  /** Category of interest */
  category?: CategoryCode;
  /** Confirmation number */
  confirmationNumber?: string;
  /** Customer */
  customer?: Organization | Person;
  /** Discount */
  discount?: number | string;
  /** Discount percent */
  discount?: number;
  /** Due date */
  dueDate?: string;
  /** Entity serving */
  minimumPaymentDue?: MonetaryAmount;
  /** Number of periods */
  numberOfPeriods?: number;
  /** Payment due */
  paymentDue?: string;
  /** Payment terms */
  paymentTerms?: string;
  /** Payment method */
  paymentMethod?: PaymentMethod;
  /** Payment ID */
  paymentMethodId?: string;
  /** Payment status */
  paymentStatus?: string;
  /** Fullfilment */
  providesService?: Organization;
  /** Purchase order reference */
  purchaseOrderRef?: string;
  /** Reference order */
  order?: Order;
  /** Has part */
  referencesOrder?: Order;
  /** Business function */
  scheduledPaymentDate?: string;
  /** Status of invoice */
  totalPaymentDue?: MonetaryAmount;
  /** Transaction ID */
  transactionId?: string;
}

/** Bid/quote */
interface PriceEstimate extends Thing {
  /** Highest price */
  highPrice?: number | string;
  /** Price quote */
  price?: number | string;
  /** Lowest price */
  lowPrice?: number | string;
  /** Pricing model */
  pricingSpecification?: PriceSpecification;
}

/** Request for price quotes */
interface QuoteDriver extends Thing {
}

/** Tender */
interface Tender extends Thing {
  /** Bidder */
  bidSubmissionDeadline?: string;
  /** Method of submission */
  bidWindow?: string;
  /** Extra qualifications */
  qualificationBidders?: Organization;
  /** Requirements */
  requirements?: string;
  /** Tender for */
  tenderFor?: string;
  /** Winner */
  winner?: Organization;
}

/** Grant or award */
interface Grant extends Thing {
  /** Funding amount */
  fundedAmount?: number | MonetaryAmount;
  /** Sponsor */
  sponsor?: Organization | Person;
  /** Website */
  url?: string;
}

/** Demand: request for offers */
interface Demand extends Thing {
  /** Accepted payment method */
  acceptedPaymentMethod?: PaymentMethod;
  /** Advance booking */
  advanceBookingTime?: string;
  /** Availability */
  availability?: ItemAvailability;
  /** Availability starts */
  availabilityEnds?: string;
  /** Available from */
  availableFrom?: string;
  /** Available through */
  availableThrough?: string;
  /** Business function */
  businessFunction?: BusinessFunction;
  /** Delivery method */
  deliveryMethod?: DeliveryMethod;
  /** Eligible quantity */
  eligibleQuantity?: QuantitativeValue;
  /** Price */
  eligibleTransactionVolume?: PriceSpecification;
  /** Customer */
  itemOffered?: Product | Service;
  /** Member of */
  memberOf?: Organization | ProgramMembership;
  /** Minimum price */
  minimumPrice?: MonetaryAmount;
  /** Availability */
  validFrom?: string;
  /** Valid through */
  validThrough?: string;
  /** Volume pricing */
  volume?: QuantitativeValue;
}

// =============================================================================
// SCHEMA.ORG ALERTS AND NOTIFICATIONS
// =============================================================================

/** An alert */
interface ActivationWebhook extends Thing {
  /** Target URL */
  targetUrl?: string;
  /** HTTP method */
  httpMethod?: string;
  /** Request body */
  httpRequestBody?: string;
  /** Request headers */
  httpRequestHeaders?: string;
  /** How to authenticate */
  authentication?: string;
}

/** Intent to receive webhooks */
interface WebhookEndpoint extends Thing {
  /** Authorization header credentials */
  authenicationTypeDefinition?: string;
  /** Property to be passed */
  explicitAuth?: string;
  /** Target callback */
  targetUrl?: string;
}

// =============================================================================
// SCHEMA.ORG DATA FEED
// =============================================================================

/** Data feed */
interface DataFeed extends Thing {
  /** Data feed item */
  dataFeedElement?: DataFeedItem[] | DataFeedItem;
}

/** Data feed item */
interface DataFeedItem extends Thing {
  /** Item in feed */
  item?: string | Thing;
  /** Date */
  dateModified?: string;
  /** Target entity */
  target?: string;
}

// =============================================================================
// SCHEMA.ORG BIDDING
// =============================================================================

/** Auction/listing for bids */
interface Auction extends Thing {
  /** Highest bid */
  highBid?: number | QuantitativeValue;
  /** Number of bids */
  numBids?: QuantitativeValue;
  /** Reserve price */
  reservePrice?: number;
  /** Starting price */
  startingPrice?: number;
}

// =============================================================================
// SCHEMA.ORG PROGRAMS
// =============================================================================

/** Loyalty program */
interface ProgramMembership extends Thing {
  /** Member number */
  membershipNumber?: string;
  /** Program name */
  programName?: string;
  /** Benefits of membership */
  member?: Organization;
  /** Program started */
  startDate?: string;
  /** Program ends */
  endDate?: string;
}

/** A discount */
interface Discount extends Thing {
  /** Discount type */
  discountType?: string;
  /** Discount code */
  discountCode?: string;
}

// =============================================================================
// SCHEMA.ORG COLLECTIONS
// =============================================================================

/** Collection of items */
interface Collection extends Thing {
  /** Collection of items */
  collectionSize?: number;
}

/** A page or collection of items */
interface CollectionPage extends CreativeWork {
  /** Collection size */
  collectionSize?: number;
}

// =============================================================================
// SCHEMA.ORG ASSESSMENTS
// =============================================================================

/** Property assessment */
interface PropertyAssessment extends Thing {
  /** New value */
  newValue?: number;
  /** Assessor */
  assessedBy?: Organization;
  /** Property assessed */
  assessedItem?: string;
}

// =============================================================================

// =============================================================================
// EXPORTS - All Schema.org types
// =============================================================================

export type {
  // Core
  Thing,
  
  // Creative Works
  CreativeWork,
  Article,
  BlogPosting,
  BlogPost,
  Review,
  MediaObject,
  ImageObject,
  AudioObject,
  VideoObject,
  SoftwareSourceCode,
  SoftwareApplication,
  VideoGameApplication,
  Movie,
  TVSeries,
  Episode,
  Course,
  CourseInstance,
  Recipe,
  HowTo,
  HowToStep,
  MusicGroup,
  MusicRecording,
  MusicAlbum,
  Map,
  MenuSection,
  MenuItem,
  Quiz,
  Question,
  Answer,
  Comment,
  Comment,
  
  // Events
  Event,
  PublicationEvent,
  CourseInstance,
  ScheduledEvent,
  BroadcastEvent,
  BroadcastService,
  
  // Organizations & People
  Organization,
  Corporation,
  GovernmentOrganization,
  NonProfitOrganization,
  Airline,
  SportsTeam,
  Person,
  
  // Places
  Place,
  Accommodation,
  Hotel,
  Restaurant,
  LocalBusiness,
  Apartment,
  House,
  
  // Products & Services
  Product,
  Service,
  Offer,
  Demand,
  ProductModel,
  PriceSpecification,
  MonetaryAmount,
  QuantitativeValue,
  
  // Medical
  Drug,
  MedicalEntity,
  MedicalCondition,
  
  // Reservations
  Reservation,
  FlightReservation,
  LodgingReservation,
  Order,
  Invoice,
  
  // Misc
  PostalAddress,
  GeoCoordinates,
  GeoShape,
  OpeningHoursSpecification,
  Rating,
  AggregateRating,
  Brand,
  ContactPoint,
  PropertyValue,
}